
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "bank_d"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )


if __name__ == "__main__":
    try:
        conn = connect_db()
        print("Database connected successfully!")
        conn.close()
    except Exception as error:
        print("Database connection failed:", error)