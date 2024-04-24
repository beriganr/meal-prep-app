from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import requests

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///recipes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    cache_key = db.Column(db.String(255), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET'])
def search_recipes():
    ingredients = [request.args.get(f'ingredient{i}') for i in range(1, 4) if request.args.get(f'ingredient{i}')]
    
    if not any(ingredients):
        return "Please provide at least one ingredient.", 400
    diet = request.args.get('diet', '')
    number_of_recipes = request.args.get('number', 10, type=int)

    cache_key = '-'.join(sorted(filter(None, ingredients))) + f"-{diet}-{number_of_recipes}"
    cached_recipes = Recipe.query.filter_by(cache_key=cache_key).all()

    if cached_recipes:
        return render_template('results.html', recipes=cached_recipes)

    api_key = '1f70087e87c54d0a93c39be96d39bdff'
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        'apiKey': api_key,
        'ingredients': ','.join(ingredients),
        'number': number_of_recipes,
        'diet': diet
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipes = response.json()
        for recipe_data in recipes:
            new_recipe = Recipe(title=recipe_data['title'], image=recipe_data['image'], cache_key=cache_key)
            db.session.add(new_recipe)
        db.session.commit()
        return render_template('results.html', recipes=Recipe.query.filter_by(cache_key=cache_key).all())
    else:
        return render_template('results.html', error='Failed to fetch recipes from API')

if __name__ == '__main__':
    app.run(debug=True)

