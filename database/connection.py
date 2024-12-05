"""
Creates/connect a connection object to the SQLite database with row factory enabled.
"""

import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables overriding default values
load_dotenv(override=True)

db_path = os.getenv('SQLITE_DB_PATH', '/home/site/wwwroot/rental.db')

def create_connection():
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection
