import psycopg2

DB_CONFIG = {
    "dbname": "cnc_pipeline",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)