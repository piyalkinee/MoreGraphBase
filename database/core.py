import databases
from neo4j import GraphDatabase

DB_NAME = "morebasedb"

POSTGRE_DATABASE_URL = f"postgresql://postgres:1231@localhost/{DB_NAME}"
NEO4J_DATABASE_URL = "bolt://localhost:7687"

database_postgre = databases.Database(POSTGRE_DATABASE_URL)
neo4j_driver = GraphDatabase.driver(NEO4J_DATABASE_URL, auth=("neo4j", "1231"))

#POSTGRE

async def connect_postgre():
    return await database_postgre.connect()

async def disconnect_postgre():
    await database_postgre.disconnect()

#NEO4J

def connect_neo4j():
    return neo4j_driver.session(database=DB_NAME)

def disconnect_neo4j():
    neo4j_driver.close()

