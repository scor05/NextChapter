""" 
Archivo que ejecuta automáticamente la aplicación y descarga todas las dependencias necesarias.
"""

import os
import subprocess

pythonDeps = ["fastapi", "uvicorn", "pydantic", "controller", "typing", "bcrypt", "psycopg2", "neo4j", "collections"]
jsDeps = ["axios", "qs"]

# Crear un archivo para que no trate de instalar todas las dependencias cada vez que se ejecuta el código.
installed = False
try:
    open("depsInstalled.txt", "x")
except FileExistsError as e:
    installed = True

if not installed:
    for pyDep in pythonDeps:
        os.system(f"pip install {pyDep}")
    for jsDep in jsDeps:
        os.system(f"npm install {jsDep}")
    open("depsInstalled", "w").close()

subprocess.Popen("python backend/driver.py")
subprocess.Popen("npm run dev", shell = True)