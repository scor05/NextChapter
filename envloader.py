from dotenv import load_dotenv
import os

load_dotenv()

NEO_USER = os.getenv("NEO4J_USERNAME")
NEO_PASS = os.getenv("NEO4J_PASSWORD")
NEO_URI = os.getenv("NEO4J_URI")
