from neo4j import GraphDatabase
from envloader import NEO_USER, NEO_PASS, NEO_URI
import colorama


'''
Notas de las querys de Neo4J:
Funcionan como asignando una variable y luego sus características: "x":Libro {name: "A"}
Algunas de estas son:

CREATE (a:Libro {titulo: 'Dune', genero: 'Ciencia Ficción'})  -> Crea un nuevo nodo
CREATE (a) - [:*RELACIÓN* {similitud = s_ij}] -> (b) -> Crea una arista entre a y b con una similitud "s_ij"
MATCH (n:Libro {titulo: '1984'}) RETURN n  -> Busca un nodo que tenga el título 1984 y que sea un libro

Para borrar, primero se hace un match y luego:
DETACH DELETE *libro encontrado*
'''

class Libro:    
    def __init__(self, name, length, author, year, genres):  # length = n páginas; genres -> array[String] de géneros del libro
        self.name = name;
        self.length = length;
        self.author = author;
        self.year = year;
        self.genres = genres;
        
        
        
with GraphDatabase.driver(uri = NEO_URI, auth = (NEO_USER, NEO_PASS)) as driver:
    try:
        colorama.init(autoreset=True)
        driver.verify_connectivity()
        print(colorama.Fore.GREEN + "Neo4J connection successful")
        driver.verify_authentication()
        print(colorama.Fore.GREEN + "Neo4J authentication successful")
        l1 = Libro("El Gran Diseño", 251, "Stephen Hawking", 2010, ["science", "physics", "philosophy"])
        driver.execute_query( 
            """
            CREATE (:Libro {name: $name, length: $length, author: $author, year: $year, genres: $genres})
            """,
            name=l1.name,
            length=l1.length,
            author=l1.author,
            year=l1.year,
            genres=l1.genres,
            database_="neo4j"
        )
        print(colorama.Fore.GREEN + "Nodo de libro creado con éxito")
    except Exception as e:
        print(colorama.Fore.RED + f"Error: {e}")
        



