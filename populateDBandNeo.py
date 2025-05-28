from envloader import *

import psycopg2
import bcrypt

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
