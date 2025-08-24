from dotenv import load_dotenv
import os
load_dotenv()

import psycopg

try:
    with psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 'Hello World!' as greeting;")
            greeting = cur.fetchone()
            print(f"Database says: {greeting[0]}")
except psycopg.OperationalError as e:
    print(f"Connection failed: {e}")
