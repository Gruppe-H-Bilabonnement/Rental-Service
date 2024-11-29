"""
Creates/connect a connection object to the SQLite database with row factory enabled.
"""

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'rental.db')

def create_connection():
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        return connection
