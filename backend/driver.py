from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from controller import insertarUsuario, getUsuarios, obtener_libros_objetos, hashPassword, deHashPassword
import bcrypt

app = FastAPI()

# Modelos para el frontend
class UsuarioRegistro(BaseModel):
    nombre: str
    correo: str
    contraseña: str

class UsuarioLogin(BaseModel):
    correo: str
    contraseña: str

class UsuarioModificacion(BaseModel):
    id: int
    nombre: str | None = None
    correo: str | None = None
    contraseña: str | None = None
    favoritos: list[str] | None = None

# ENDPOINTS
@app.post("/api/register")
def register(usuario: UsuarioRegistro):
    try:
        insertarUsuario(usuario.nombre, usuario.correo, usuario.contraseña, [])
        return {"mensaje": "Usuario creado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/login")
def login(usuario: UsuarioLogin):
    usuarios = getUsuarios()
    for u in usuarios:
        id_db, nombre_db, correo_db, contraseña_hash, favoritos = u
        if correo_db == usuario.correo:
            if bcrypt.checkpw(usuario.contraseña.encode("utf-8"), contraseña_hash.encode("utf-8")):
                return {"id": id_db, "nombre": nombre_db, "correo": correo_db, "favoritos": favoritos}
            else:
                raise HTTPException(status_code=401, detail="Contraseña incorrecta.")
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")

@app.get("/api/libros")
def obtener_libros():
    libros = obtener_libros_objetos()
    return [
        {
            "titulo": libro.name,
            "autores": libro.authors,
            "generos": libro.genres,
            "anio": libro.year,
            "paginas": libro.length
        }
        for libro in libros
    ]
