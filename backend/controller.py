from envloader import *
import psycopg2
from neo4j import GraphDatabase
import bcrypt
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
            RETURN l.titulo AS titulo, l.autores AS autores, l.generos AS generos,
                   l.anio AS anio, l.paginas AS paginas
        """)
        return result

    with driver.session() as session:
        result = session.execute_read(fetch)
        for record in result:
            libro = Libro(
                name=record["titulo"],
                length=record["paginas"],
                authors=record["autores"],
                year=record["anio"],
                genres=record["generos"]
            )
            libros.append(libro)

    return libros
