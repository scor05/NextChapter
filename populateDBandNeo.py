from envloader import *
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
#userDBCursor.execute("""
        #CREATE TABLE IF NOT EXISTS usuarios (
        #    id SERIAL PRIMARY KEY,
        #    nombre VARCHAR(100) NOT NULL,
         #   correo VARCHAR(100) UNIQUE NOT NULL,
          #  contraseña TEXT NOT NULL,
           # favoritos TEXT[] DEFAULT '{}'
        #);
    #""")

# Métodos para crear, borrar, modificar y traer todos los usuarios de postgres:

def insertarUsuario(nombre, correo, contraseña, favoritos):
    try:
        hashed_password = hashPassword(contraseña)
        userDBCursor.execute("""
            INSERT INTO usuarios (nombre, correo, contraseña, favoritos)
            VALUES (%s, %s, %s, %s)
        """, (nombre, correo, hashed_password, favoritos))
        print("Usuario insertado con contraseña protegida.")
    except Exception as e:
        print("Error al insertar usuario: ", e)
    
        
# bcrypt hashing:
def hashPassword(password):
    hashedPass = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashedPass

def deHashPassword(password):
    return password.decode("utf-8")

def getUsuarios():
    result = []
    try:
        userDBCursor.execute("SELECT * FROM usuarios;")
        for fila in userDBCursor.fetchall():
            result.append(fila)
    except Exception as e:
        print("Error al obtener usuarios: ", e)
    return result

def eliminarUsuario(usuario_id):
    userDBCursor.execute("SELECT 1 FROM usuarios WHERE id = %s", (usuario_id))
    if userDBCursor.fetchone(): 
        userDBCursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id))
    else:
        print("Error al eliminar usuario: Usuario no encontrado en la base de datos.")
    

def modificarUsuario(usuario_id, nuevo_nombre, nuevo_correo, nueva_contraseña, nuevos_favoritos):
    try:
        campos = []
        valores = []

        if nuevo_nombre is not None:
            campos.append("nombre = %s")
            valores.append(nuevo_nombre)

        if nuevo_correo is not None:
            campos.append("correo = %s")
            valores.append(nuevo_correo)

        if nueva_contraseña is not None:
            campos.append("contraseña = %s")
            valores.append(hashPassword(nueva_contraseña))

        if nuevos_favoritos is not None:
            campos.append("favoritos = %s")
            valores.append(nuevos_favoritos)

        if not campos:
            return

        valores.append(usuario_id)

        query = f"""
            UPDATE usuarios
            SET {', '.join(campos)}
            WHERE id = %s
        """
        userDBCursor.execute(query, tuple(valores))
    except Exception as e:
        print("Error al modificar usuario: ", e)
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
    w_gen = 0.4
    w_año = 0.2
    w_autor = 0.2
    w_len = 0.2
    año_max_dif = 150
    length_max_dif = 1000
    
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

    # Longitud
    if libroA.length is not None and libroB.length is not None:
        dif_len = min(abs(libroA.length - libroB.length) / length_max_dif, 1)
    else:
        dif_len = 0

    dissimilitud = (
        w_gen * (1 - sim_generos) + 
        w_año * dif_año + 
        w_autor * (1 - sim_autor) + 
        w_len * dif_len
    )
    return round(max(0, 1 - dissimilitud), 4)

# Función para ejecutar las querys de Cypher para crear dos libros con un peso (score) dado.
def crear_libro_y_relacion(tx, libroA, libroB, score):
    tx.run("""
    MERGE (a:Libro {titulo: $tituloA})
      SET a.autores = $autoresA, a.generos = $generosA, a.anio = $anioA, a.paginas = $paginasA
    MERGE (b:Libro {titulo: $tituloB})
      SET b.autores = $autoresB, b.generos = $generosB, b.anio = $anioB, b.paginas = $paginasB
    MERGE (a)-[:RELACIONADO_CON {similitud: $score}]->(b)
    """,
    tituloA=libroA.name,
    autoresA=libroA.authors,
    generosA=libroA.genres,
    anioA=libroA.year,
    paginasA=libroA.length,
    tituloB=libroB.name,
    autoresB=libroB.authors,
    generosB=libroB.genres,
    anioB=libroB.year,
    paginasB=libroB.length,
    score=score)

# Poblar Neo4J con algorítmo de "K" vecinos
app = FastAPI()
@app.post("/cargar_libros")
def cargar_libros():
    temas = ["fantasy", "science_fiction", "horror", "romance", "historical_fiction"]
    libros = []

    for tema in temas:
        r = requests.get(f"https://openlibrary.org/subjects/{tema}.json?limit=20")
        for d in r.json().get("works", []):
            name = d.get("title")
            authors = [a.get("name") for a in d.get("authors", []) if a.get("name")]
            year = d.get("first_publish_year")
            genres = d.get("subject", [])
            libro = Libro(name, None, authors, year, genres)
            libros.append(libro)

    # Algoritmo K Vecinos
    K = 4
    with driver.session() as session:
        for libroA in libros:
            similitudes = []
            for libroB in libros:
                if libroA.name != libroB.name:
                    s = similitud(libroA, libroB)
                    similitudes.append((libroB, s))
            top_k = sorted(similitudes, key=itemgetter(1), reverse=True)[:K]
            for libroB, s in top_k:
                session.execute_write(crear_libro_y_relacion, libroA, libroB, s)

    return {"mensaje": f"Se cargaron {len(libros)} libros y se conectaron por similitud."}

message = cargar_libros()
print(message)