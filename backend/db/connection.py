import os
import psycopg2

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "cnc_pipeline"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)