"""
Creates/connect a connection object to the SQLite database with row factory enabled.
"""

from dotenv import load_dotenv
import sqlite3
import os

# Load environment variables from .env file
load_dotenv()

# Read database path from the environment variable or use the default path
DB_PATH = os.getenv('SQLITE_DB_PATH')

def create_connection():
    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e.args}")
        return None
