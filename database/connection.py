"""
Creates/connect a connection object to the SQLite database with row factory enabled.
"""

import sqlite3

def create_connection():
    connection = sqlite3.connect('database/rental.db')
    connection.row_factory = sqlite3.Row
    return connection
