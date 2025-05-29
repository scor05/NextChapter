from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from controller import *
import bcrypt
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return {"mensaje": "Usuario creado exitosamDente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/login")
def login(usuario: UsuarioLogin):
    user_data = getUsuario(usuario.correo)
    if user_data is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    id, nombre, correo, hashed_password, favoritos = user_data
    if not bcrypt.checkpw(usuario.contraseña.encode('utf-8'), hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta.")

    return {
        "mensaje": "Login exitoso.",
        "usuario": {
            "nombre": nombre,
            "correo": correo,
            "favoritos": favoritos
        }
    }

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


if __name__ == "__main__":
    uvicorn.run("driver:app", host="0.0.0.0", port=8000, reload=True)