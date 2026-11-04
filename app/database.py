import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def get_database_path():
    return os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "submissions.db")
    )


def get_connection():
    connection = sqlite3.connect(get_database_path())
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                registration_number TEXT NOT NULL,
                assignment_title TEXT NOT NULL,
                submission_url TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()