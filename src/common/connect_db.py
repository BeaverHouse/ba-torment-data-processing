import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_postgres() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DBNAME"),
    )

def get_postgres_client() -> psycopg2.extensions.cursor:
    return get_postgres().cursor()

