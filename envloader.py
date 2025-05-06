from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("NEO4J_USERNAME")
DB_PASS = os.getenv("NEO4J_PASSWORD")
DB_URI = os.getenv("NEO4J_URI")
