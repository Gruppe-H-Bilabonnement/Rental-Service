from flask import Flask, jsonify

# create a Flask app
app = Flask(__name__)

# @swag_from('swagger/docs/home.yml)
@app.route('/')
def home():
    return jsonify({'message': 'Rental Service API'})

# run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)