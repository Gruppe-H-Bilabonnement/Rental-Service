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
import sys
import sqlite3
from dotenv import load_dotenv
import pandas as pd
from database.connection import create_connection
import requests
from io import BytesIO

# Initialize the database
def init_db():
    _create_table()

    # Check if data exists to avoid reinitialization
    if not _check_data_exists():
        _load_rental_data()
        print("Database initialized successfully with data.")
    else:
        print("Database already initialized. No action taken.")

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
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

# Check if rental data already exists in the database
def _check_data_exists():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) AS count FROM rental_contracts")
        result = cursor.fetchone()['count'] > 0
        
        return result
    except sqlite3.Error as e:
        return False
    finally:
        connection.close()

def _load_rental_data():
    # GitHub raw URL for the Excel file
    excel_url = 'https://raw.githubusercontent.com/Gruppe-H-Bilabonnement/RentalService/main/data-files/Bilabonnement_2024_Clean.xlsx'

    try:
        # Download the Excel file from GitHub
        response = requests.get(excel_url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Critical: Failed to download Excel file from {excel_url}")
            return

        # Read the Excel file directly into a pandas DataFrame from the byte content
        data = pd.read_excel(BytesIO(response.content))

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

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from GitHub: {e}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
 