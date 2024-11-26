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

from flask import Flask, jsonify
from database.initialization import init_db
from api.rental_routes import rental_routes

app = Flask(__name__)

# Register rental routes
app.register_blueprint(rental_routes, url_prefix='/api/v1/rentals')

# home route with api documentation
@app.route('/api/v1/')
def home():
    return jsonify({
        "message": "Welcome to RentalService API",
        "documentation": "in progress.."
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
    app.run(host='0.0.0.0', port=80)
