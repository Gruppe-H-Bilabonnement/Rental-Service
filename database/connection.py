"""
Creates/connect a connection object to the SQLite database with row factory enabled.
"""

import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Read database path from the environment variable or use the default path
db_path = os.getenv('SQLITE_DB_PATH', '/home/rental.db')

def create_connection():
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e.args}")
