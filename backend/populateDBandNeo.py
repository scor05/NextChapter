from envloader import *
import psycopg2
from neo4j import GraphDatabase
import bcrypt
from operator import itemgetter
from fastapi import FastAPI
import requests
from Libro import Libro

# Conexión de postgres (NOTA: Usamos railway para hostear la DB)
userDBConnection = psycopg2.connect(
    host = DB_HOST,
    port = DB_PORT,
    dbname = DB_NAME,
    user = DB_USER,
    password = DB_PASSWORD
)

userDBConnection.autocommit = True
userDBCursor = userDBConnection.cursor()

# Crear tabla base (ya ejecutado el código no se requiere de volver a ejecutar)
userDBCursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            favoritos TEXT[] DEFAULT '{}'
        );
    """)

# NEO4J
driver = GraphDatabase.driver(uri = NEO_URI, auth = (NEO_USER, NEO_PASS))
driver.verify_connectivity()

# Función Jaccard que permite calcular la similitud entre dos sets sin importar de qué son.
def jaccard(set1, set2):
    inter = len(set1 & set2)
    union = len(set1 | set2)
    return inter / union if union else 0

# Función similitud modificada ya para que acepte varios autores y adaptada para que tenga un rango de [0,1]:
# sim(A,B) = 1 - [sim_generos + sim_año + sim_autor + sim_len]
# Donde:
# sim_generos = w_gen * (1 - Jaccard(generosA, generosB))
# sim_año = w_año * (abs(añoA - añoB) / intervaloAños)
# sim_autor = w_autor * (1 - Jaccard(autoresA, autoresB))
# sim_len = w_len * (abs(lenA - lenB) / intervaloLen))
def similitud(libroA, libroB):
    
    # CONSTANTES (SE PUEDEN MODIFICAR SI NO TIRA BUENAS RECOMENDACIONES)
    w_gen = 0.5
    w_año = 0.3
    w_autor = 0.2
    año_max_dif = 150
    
    # Géneros
    generosA = set(libroA.genres)
    generosB = set(libroB.genres)
    sim_generos = jaccard(generosA, generosB)

    # Años de publicación
    if libroA.year is None or libroB.year is None:
        dif_año = 1
    else:
        dif_año = min(abs(libroA.year - libroB.year) / año_max_dif, 1)

    # Autores
    autoresA = set(a.lower() for a in libroA.authors)
    autoresB = set(b.lower() for b in libroB.authors)
    sim_autor = jaccard(autoresA, autoresB)


    dissimilitud = (
        w_gen * (1 - sim_generos) + 
        w_año * dif_año + 
        w_autor * (1 - sim_autor)
    )
    return round(max(0, 1 - dissimilitud), 4)

# Función para ejecutar las querys de Cypher para crear dos libros con un peso (score) dado.
def crear_libro_y_relacion(tx, libroA, libroB, score):
    tx.run("""
    MERGE (a:Libro {titulo: $tituloA})
    SET a.autores = $autoresA, a.generos = $generosA, a.anio = $anioA
    MERGE (b:Libro {titulo: $tituloB})
    SET b.autores = $autoresB, b.generos = $generosB, b.anio = $anioB
    MERGE (a)-[:RELACIONADO_CON {similitud: $score}]->(b)
    """,
    tituloA=libroA.name,
    autoresA=libroA.authors,
    generosA=libroA.genres,
    anioA=libroA.year,
    tituloB=libroB.name,
    autoresB=libroB.authors,
    generosB=libroB.genres,
    anioB=libroB.year,
    score=score)

# Poblar Neo4J con algorítmo de "K" vecinos

def cargar_libros():
    temas = [
        "fantasy", "science_fiction", "horror", "romance", "historical_fiction",
        "thriller", "mystery", "contemporary", "young_adult", "graphic_novels"
    ]
    libros = []

    for tema in temas:
        r = requests.get(f"https://openlibrary.org/subjects/{tema}.json?limit=50")
        for d in r.json().get("works", []):
            name = d.get("title")
            authors = [a.get("name") for a in d.get("authors", []) if a.get("name")]
            year = d.get("first_publish_year")
            genres = d.get("subject", [])
            libro = Libro(name, authors, year, genres)
            libros.append(libro)
            
            # filtro para que no salgan tantos libros del siglo XIX
            if year and year >= 1950 and name and authors and genres:
                libro = Libro(name, authors, year, genres)
                libros.append(libro)
                
    # obtener títulos ya existentes para repoblar con libros más recientes
    with driver.session() as session:
        existing_result = session.run("MATCH (l:Libro) RETURN l.titulo AS titulo, l.autores AS autores, l.anio AS anio, l.generos AS generos")
        existentes = []
        for record in existing_result:
            existentes.append(
                Libro(
                    name=record["titulo"],
                    authors=record["autores"] or [],
                    year=record["anio"],
                    genres=record["generos"] or []
                )
            )
        existentes_nombres = set([libro.name for libro in existentes])
        nuevos_libros = [libro for libro in libros if libro.name not in existentes_nombres]


    # Algoritmo K Vecinos (NOTA: cambiado para solo repoblar con libros más modernos)
    K = 4
    with driver.session() as session:
        for libroA in nuevos_libros:
            similitudes = []
            for libroB in existentes:
                s = similitud(libroA, libroB)
                similitudes.append((libroB, s))

            top_k = sorted(similitudes, key=itemgetter(1), reverse=True)[:K]

            for libroB, s in top_k:
                session.execute_write(crear_libro_y_relacion, libroA, libroB, s)

    return {"mensaje": f"Se cargaron {len(libros)} libros y se conectaron por similitud."}

message = cargar_libros()
print(message)