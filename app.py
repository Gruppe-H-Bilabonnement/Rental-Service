"""
RentalService API

This module initializes and runs the RentalService Flask application. It sets up the necessary routes, error handlers, and initializes the database.

Routes:
    /api/v1/ - Home route with API documentation.
    /api/v1/rentals - Rental routes registered from rental_routes blueprint.

Error Handlers:
    404 - Returns a JSON response with an error message for Not Found.
    500 - Returns a JSON response with an error message for Internal Server Error.

Initialization:
    init_db() - Initializes the database.
    app.run() - Runs the Flask application on host '0.0.0.0' and port 80.
"""

import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flasgger import swag_from
from database.initialization import init_db
from api.rental_routes import rental_routes
from swagger.config import init_swagger

app = Flask(__name__)

# App Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
port = int(os.getenv('PORT', 80))

# Swagger Documentation
swagger = init_swagger(app)

# Register rental routes
app.register_blueprint(rental_routes, url_prefix='/api/v1/rentals')

# Home route with API documentation
@app.route('/api/v1/')
@swag_from('swagger/docs/home.yml')
def home():
    return jsonify({
        "message": "Welcome to RentalService API",
        "endpoints": [
            {
                "method": "GET",
                "endpoint": "/api/v1/",
                "description": "Provides an overview of the API and its endpoints"
            },
            {
                "method": "POST",
                "endpoint": "/api/v1/rentals",
                "description": "Create a new rental contract"
            },
            {
                "method": "GET",
                "endpoint": "/api/v1/rentals/all",
                "description": "Retrieve all rental contracts"
            },
            {
                "method": "GET",
                "endpoint": "/api/v1/rentals/<int:rental_id>",
                "description": "Retrieve a rental contract by its ID"
            },
            {
                "method": "PATCH",
                "endpoint": "/api/v1/rentals/<int:rental_id>",
                "description": "Update an existing rental contract by its ID"
            },
            {
                "method": "DELETE",
                "endpoint": "/api/v1/rentals/<int:rental_id>",
                "description": "Delete a rental contract by its ID"
            }
        ]
    })

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Initialize database and run the app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=port)
