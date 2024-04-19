from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests

app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model definition
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    cache_key = db.Column(db.String(255), nullable=True)

# Manually push application context and create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Meal Prep App!"

@app.route('/search', methods=['GET'])
def search_recipes():
    ingredients = request.args.get('ingredients', '').split(',')
    if len(ingredients) > 3:
        return jsonify({"error": "Maximum of 3 ingredients allowed"}), 400

    cache_key = '-'.join(sorted(ingredients))
    cached_recipes = Recipe.query.filter_by(cache_key=cache_key).all()
    if cached_recipes:
        return jsonify([{'id': r.id, 'title': r.title, 'image': r.image} for r in cached_recipes])

    api_key = '1f70087e87c54d0a93c39be96d39bdff'
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {'apiKey': api_key, 'ingredients': ','.join(ingredients), 'number': '10'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        recipes = response.json()
        for recipe_data in recipes:
            new_recipe = Recipe(title=recipe_data['title'], image=recipe_data['image'], cache_key=cache_key)
            db.session.add(new_recipe)
        db.session.commit()
        return jsonify(recipes)
    else:
        return jsonify({'error': 'Failed to fetch recipes from API'}), response.status.code

if __name__ == '__main__':
    app.run(debug=True)
