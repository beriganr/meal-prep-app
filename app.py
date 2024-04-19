import requests
import logging
from flask import Flask, request, jsonify

api_key = '1f70087e87c54d0a93c39be96d39bdff'
url = 'https://api.spoonacular.com/recipes/complexSearch'

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return "Welcome to the Meal Prep App!"

@app.route('/search', methods=['GET'])
def search_recipes():
    ingredient = request.args.get('ingredient')
    number_of_recipes = request.args.get('num_recipes', default=10, type=int)
    params = {
        'apiKey': api_key,
        'query': ingredient,
        'number': number_of_recipes
    }
    response = requests.get(url, params=params)
    logging.debug(f"URL Requested: {response.url}")
    logging.debug(f"Status Code: {response.status_code}")
    logging.debug(f"Response: {response.text}")
    if response.status_code == 200:
        return jsonify(response.json()['results'])
    else:
        return jsonify({'error': 'Failed to fetch recipes'}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)
