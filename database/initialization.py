"""
This module initializes the rental service database by creating necessary tables and loading initial data from a CSV file.

Functions:
    init_db(): Initializes the database by creating tables and loading data if not already present.
    _create_table(): Creates the rental_contracts table and associated indexes if they do not exist.
    _check_data_exists(): Checks if rental data already exists in the rental_contracts table.
    _load_rental_data(): Loads rental data from a CSV file into the rental_contracts table.

Dependencies:
    - os: For file path operations.
    - sqlite3: For SQLite database operations.
    - pandas: For reading and processing CSV files.
    - create_connection: Custom function from database.connection module to establish a database connection.
"""

import os
import sqlite3
from dotenv import load_dotenv
import pandas as pd
from database.connection import create_connection
import requests

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize the database
def init_db():
    print("Initializing database...")
    try:
        # Check if the database is already initialized
        if not _check_data_exists():
            _create_table()
            _load_rental_data()
            print("Database initialized successfully with data.")
        else:
            print("Database already initialized. No action taken.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Creates the rental_contracts table
def _create_table():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Define the rental_contracts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rental_contracts(
                id INTEGER PRIMARY KEY,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL CHECK (end_date > start_date),
                start_km INTEGER NOT NULL CHECK (start_km >= 0),
                contracted_km INTEGER NOT NULL CHECK (contracted_km >= 0),
                monthly_price REAL NOT NULL CHECK (monthly_price >= 0),
                car_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL
            )
        """)

        # Indexes for efficient queries on car_id and customer_id
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_car_id ON rental_contracts(car_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_customer_id ON rental_contracts(customer_id)
        """)

        connection.commit()
        connection.close()
        print("Table created successfully or already exists.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    except Exception as e:
        print(f"Unexpected error creating table: {e}")

# Check if rental data already exists in the database
def _check_data_exists():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM rental_contracts")
        result = cursor.fetchone()  # Fetch the first column of the result (COUNT)
        return result[0] > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error checking data: {e}")
        return False
    finally:
        connection.close()

def _load_rental_data():
    # Read the Excel file path from the environment variable or use the default path
    excel_path = os.getenv('XLSX_PATH', '/app/Bilabonnement_2024_Clean.xlsx')

    try:
       
        # Read the Excel file directly into a pandas DataFrame from the byte content
        data = pd.read_excel(excel_path)

        # Prepare data for insertion (a list of tuples for batch insertion)
        rental_data = []
        car_id_counter = 1  # TODO: Implement a way to generate unique car IDs
        customer_id_counter = 1  # TODO: Implement a way to generate unique customer IDs

        for _, row in data.iterrows():
            # Convert dates safely
            start_date = pd.to_datetime(row['Start abonnement Dato'], dayfirst=True).strftime('%Y-%m-%d')
            end_date = pd.to_datetime(row['Slut Dato Abonnement Periode'], dayfirst=True).strftime('%Y-%m-%d')

            # Convert numeric values safely
            start_km = int(row['Koert Km ved abonnemt start'])
            contracted_km = int(row['Aftalt kontraktabonnment KM'])
            monthly_price = float(row['abonnement pris pr maened'])

            # Append data tuple for batch insertion
            rental_data.append((
                start_date,
                end_date,
                start_km,
                contracted_km,
                monthly_price,
                car_id_counter,
                customer_id_counter
            ))

            # Increment car_id and customer_id for each row
            car_id_counter += 1
            customer_id_counter += 1

        # Connect to the SQLite database
        connection = create_connection()
        cursor = connection.cursor()

        # Insert the data into the rental_contracts table with executemany for efficiency
        cursor.executemany("""
            INSERT INTO rental_contracts (
                start_date, end_date, start_km, contracted_km, 
                monthly_price, car_id, customer_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rental_data)

        connection.commit()
        connection.close()
        print(f"{len(rental_data)} rows inserted successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e.args}")
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
 