"""
Creates/connect a connection object to the SQLite database with row factory enabled.
"""

import sqlite3
import os

# Read database path from the environment variable or use the default path
db_path = os.getenv('DB_PATH', 'database/rental.db')

def create_connection():
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection
