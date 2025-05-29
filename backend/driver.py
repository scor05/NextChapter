from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from controller import *
from typing import List, Optional
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
    nombre: Optional[str]
    correo: Optional[str]
    contraseña: Optional[str]
    favoritos: Optional[List[str]]

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
    
    idNum, nombre, correo, hashed_password, favoritos = user_data
    if not bcrypt.checkpw(usuario.contraseña.encode('utf-8'), hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta.")

    return {
        "mensaje": "Login exitoso.",
        "usuario": {
            "id": idNum,
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
        }
        for libro in libros
    ]

@app.get("/api/recomendar")
def recomendar(correo: str):
    try:
        user_data = getUsuario(correo)
        if not user_data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        favoritos = user_data[-1]  # -1 es el último index.
        recomendaciones = recomendar_libros_por_favoritos(favoritos)
        
        # Serializar libros
        libros_json = []
        for libro in recomendaciones:
            libros_json.append({
                "titulo": libro.name,
                "generos": libro.genres[:3],  # Mostrar como máximo 3 géneros y 2 autores porque si no sería muy largo
                "autores": libro.authors[:2],
                "year": libro.year,
            })
        return libros_json

    except Exception as e:
        print("Error en /api/recomendar:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/modificar_usuario")
async def modificar_usuario(request: Request):
    try:
        raw_body = await request.body()

        data = await request.json()

        # Puedes reconstruir el modelo Pydantic a mano
        modificado = UsuarioModificacion(**data)
        modificarUsuario(modificado.id, modificado.nombre, modificado.correo, modificado.contraseña, modificado.favoritos)

        return {"mensaje": "Usuario actualizado correctamente."}
    except Exception as e:
        print("Error al procesar JSON/modificación:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/libros_favoritos")
def libros_favoritos(titulos: List[str] = Query(...)):
    try:
        todos = obtener_libros_objetos()
        filtrados = [libro for libro in todos if libro.name in titulos]
        return [
            {
                "titulo": libro.name,
                "generos": libro.genres[:5],
                "autores": libro.authors[:2],
                "year": libro.year,
            }
            for libro in filtrados
        ]
    except Exception as e:
        print("Error en /api/libros_favoritos:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/buscar")
def buscar_libros(titulo: Optional[str] = None, autor: Optional[str] = None, genero: Optional[str] = None):
    try:
        if not titulo and not autor and not genero:
            raise HTTPException(
                status_code=400,
                detail="Debe de llenar por lo menos un campo."
            )

        todos = obtener_libros_objetos()
        resultados = []
        
        for libro in todos:
            titulo_match = True
            autor_match = True
            genero_match = True
            
            if titulo:
                titulo_match = titulo.lower() in libro.name.lower()
            if autor:
                autor_match = any(autor.lower() in a.lower() for a in libro.authors)
            if genero:
                genero_match = any(genero.lower() in g.lower() for g in libro.genres)
            
            if titulo_match and autor_match and genero_match:
                resultados.append({
                    "titulo": libro.name,
                    "autores": libro.authors,
                    "generos": libro.genres,
                    "year": libro.year
                })

        return resultados
        
    except HTTPException:
        raise
    except Exception as e:
        print("Error en /api/buscar:", e)
        raise HTTPException(
            status_code=500,
            detail="Error interno al buscar libros. Por favor intente nuevamente."
        )


if __name__ == "__main__":
    uvicorn.run("driver:app", host="0.0.0.0", port=8000, reload=True)