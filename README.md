# RentalService API 🚗📊
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft%20Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)  

A robust, scalable Flask-based API for managing vehicle rental contracts, designed with modern Python development best practices.

## Project Overview

RentalService API is a comprehensive web application built to streamline rental contract management. It leverages Flask for web routing, SQLite for data persistence, and provides a clean, well-structured approach to handling rental contract operations.

## Key Features

### Technical Highlights
- **Modern Python Stack**: Utilizing Flask 3.1.0, pandas 2.2.3, and SQLite
- **RESTful API Design**: Complete CRUD operations for rental contracts
- **Automatic Database Initialization**: Dynamic data loading from Excel spreadsheets
- **Comprehensive Documentation**: Swagger/OpenAPI integration
- **Flexible Error Handling**: Structured JSON error responses
- **SQLITE**


### Functional Capabilities
- Create new rental contracts
- Retrieve all or specific rental contracts
- Update existing rental contracts
- Delete rental contracts
- Detailed API documentation

## Architectural Design

### System Components

1. **Web Framework**: Flask
   - Lightweight and flexible Python web framework
   - Provides routing and request handling

2. **Database**: SQLite
   - Embedded, serverless database
   - Automatic table creation and data initialization
   - Efficient indexing for query performance

3. **Data Processing**: Pandas
   - Excel file reading and data transformation
   - Robust data type handling

4. **Documentation**: Flasgger
   - Swagger/OpenAPI specification generation
   - Interactive API documentation

## 📂 Project Structure

```
rental-service-api/
│
├── app.py                   # Main application entry point
├── database/
│   ├── connection.py        # Database connection management
│   └── initialization.py    # Database setup and data loading
│
├── api/
│   └── rental_routes.py     # API endpoint definitions
│
├── repositories/
│   └── rental_repository.py # Database interaction methods
│
├── swagger/
│   ├── config.py            # Swagger configuration
│   └── docs/                # Swagger documentation specs
│
└── xlsx/
    └── bilabonnement_2024_Clean.xlsx  # Source data spreadsheet
```

### Try with Azure
https://group-h-rental-service-emdqb2fjdzh7ddg2.northeurope-01.azurewebsites.net/api/v1/docs#/default/get_api_v1_rentals__rental_id_

### Installation Steps Docker

...

## API Endpoints

### Base URL: `/api/v1/rentals`

| Method | Endpoint      | Description                        |
|--------|---------------|-------------------------------------|
| GET    | `/api/v1/rentals/`           | API overview and documentation      |
| POST   | `/api/v1/rentals/`           | Create a new rental contract        |
| GET    | `/api/v1/rentals/all`        | Retrieve all rental contracts       |
| GET    | `/api/v1/rentals/<id>`       | Retrieve a specific rental contract |
| PATCH  | `/api/v1/rentals/<id>`       | Update a rental contract            |
| DELETE | `/api/v1/rentals/<id>`       | Delete a rental contract            |

## Documentation

### Swagger UI
Interactive API documentation available at: `.../api/v1/docs`

## Customization

### Configuration Options

| Environment Variable | Description                  | Default Value                    |
|---------------------|------------------------------|----------------------------------|
| `SQLITE_DB_PATH`    | Path to SQLite database file | `/home/site/wwwroot/rental.db`   |


---
