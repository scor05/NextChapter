from envloader import *
import psycopg2
from neo4j import GraphDatabase
import bcrypt
from Libro import Libro
import random
from collections import Counter

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

driver = GraphDatabase.driver(uri = NEO_URI, auth = (NEO_USER, NEO_PASS))
driver.verify_connectivity()

# ---------------- FUNCIONES DE POSTGRES ------------------------
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
    return hashedPass.decode("utf-8")

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

def getUsuario(correo):
    try:
        userDBCursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = userDBCursor.fetchone()
        return usuario
    except Exception as e:
        print("Error al obtener usuario:", e)
        return None


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


# ------------------ FUNCIONES DE NEO4J -------------------------
def obtener_libros_objetos():
    libros = []

    def fetch(tx):
        result = tx.run("""
            MATCH (l:Libro)
            RETURN l.titulo AS titulo, l.autores AS autores, l.generos AS generos, l.anio AS anio
        """)
        return [record for record in result]

    with driver.session() as session:
        records = session.execute_read(fetch)

    libros = []
    for record in records:
        libros.append(
            Libro(
                name=record["titulo"],
                authors=record["autores"],
                genres=record["generos"],
                year=record["anio"],
            )
        )
    return libros

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

def similitud(libroA, libroB):
    
    # CONSTANTES (SE PUEDEN MODIFICAR SI NO TIRA BUENAS RECOMENDACIONES)
    w_gen = 0.5
    w_año = 0.2
    w_autor = 0.3
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

def recomendar_libros_por_favoritos(favoritos):
    todos_los_libros = obtener_libros_objetos()
    
    # Retorna 3 libros al azar si los favoritos están vacíos
    if not favoritos:
        return random.sample(todos_los_libros, 6)

    # Filtrar objetos Libro que están en favoritos
    libros_favoritos = [libro for libro in todos_los_libros if libro.name in favoritos]

    generos_usuario = Counter()
    for libro in libros_favoritos:
        generos_usuario.update(libro.genres)


    recomendaciones = []
    for libro in todos_los_libros:
        if libro.name in favoritos:
            continue  # no recomendar favoritos

        # Promedio de similitud con todos los favoritos
        similitudes = [similitud(libro, favorito) for favorito in libros_favoritos]
        score_promedio = sum(similitudes) / len(similitudes)
        recomendaciones.append((score_promedio, libro))

    # Ordenar por mayor similitud y devolver top 3
    recomendaciones.sort(reverse=True, key=lambda x: x[0])
    recomendados = [libro for _, libro in recomendaciones[:9]]

    return recomendados