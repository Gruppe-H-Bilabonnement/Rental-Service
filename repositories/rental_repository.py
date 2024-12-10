"""
This module provides functions to interact with the rental contracts in the database.

Functions:
- db_create_rental_contract(data): Creates a new rental contract with the provided data.
- db_get_all_rental_contracts(): Retrieves all rental contracts from the database.
- db_get_rental_by_id(rental_id): Retrieves a single rental contract by its ID.
- db_update_rental(rental_id, data): Updates an existing rental contract with the provided data.
- db_delete_rental(rental_id): Deletes a rental contract by its ID.
"""

import sqlite3
from dotenv import load_dotenv
import os

# Load envoirnment variables
load_dotenv()

SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', '/home/rental.db')

# Create a new rental contract
def db_create_rental_contract(data):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        query = """
            INSERT INTO rental_contracts (start_date, end_date, start_km, contracted_km, monthly_price, car_id, customer_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            data['start_date'],
            data['end_date'],
            data['start_km'],
            data['contracted_km'],
            data['monthly_price'],
            data['car_id'],
            data['customer_id']
        ))

        connection.commit()
        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        connection.close()

# Retrieve all rental contracts
def db_get_all_rental_contracts():
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM rental_contracts")
        rentals = cursor.fetchall()
        return [dict(row) for row in rentals]

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

# Retrieve a single rental contract by ID
def db_get_rental_contract_by_id(rental_id):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM rental_contracts WHERE id = ?", (rental_id,))
        rental = cursor.fetchone()
        return dict(rental) if rental else False

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

# Update a rental contract
def db_update_rental_contract(rental_id, data):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Get information about all columns in the rental_contracts table
        cursor.execute("PRAGMA table_info(rental_contracts)")

        # Fetch all column information
        all_columns = cursor.fetchall()

        # Extract column names from the column information
        columns = [column['name'] for column in all_columns if column['name'] not in ['id']]

        # Dynamically build the update query based on provided fields
        update_fields = []
        params = []
        for key in columns:
            if key in data:
                update_fields.append(f"{key} = ?")
                params.append(data[key])
        
        # Execute update if fields are provided
        if update_fields:
            query = f"UPDATE rental_contracts SET {', '.join(update_fields)} WHERE id = ?"
            params.append(rental_id)

            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount > 0  # Return True if rows were updated

        return False  # No valid fields to update

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        connection.close()

# Delete a rental contract
def db_delete_rental_contract(rental_id):
    try:
        connection = sqlite3.connect(SQLITE_DB_PATH)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("DELETE FROM rental_contracts WHERE id = ?", (rental_id,))
        connection.commit()
        return cursor.rowcount > 0 # Return True if rows were deleted

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()
