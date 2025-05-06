from neo4j import GraphDatabase
from envloader import DB_USER, DB_PASS, DB_URI

with GraphDatabase.driver(uri = DB_URI, auth = (DB_USER, DB_PASS)) as driver:
    try:
        driver.verify_connectivity()
        print("Conexion exitosa")
    except Exception as e:
        print(f"Error: {e}")

