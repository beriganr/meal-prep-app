from flask import Flask, request, jsonify, render_template_string
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

# Manually initialize database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Recipe Search</title>
    </head>
    <body>
        <h1>Search for Recipes</h1>
        <form method="GET" action="/search">
            <input type="text" name="ingredient1" placeholder="Ingredient 1" required>
            <input type="text" name="ingredient2" placeholder="Ingredient 2">
            <input type="text" name="ingredient3" placeholder="Ingredient 3">
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    """)

@app.route('/search', methods=['GET'])
def search_recipes():
    ingredients = [request.args.get(f'ingredient{i}') for i in range(1, 4) if request.args.get(f'ingredient{i}')]
    if len(ingredients) > 3:
        return "Maximum of 3 ingredients allowed", 400

    cache_key = '-'.join(sorted(filter(None, ingredients)))
    cached_recipes = Recipe.query.filter_by(cache_key=cache_key).all()
    if cached_recipes:
        result_html = '<h1>Recipes Found</h1>'
        for recipe in cached_recipes:
            result_html += f"<div><h2>{recipe.title}</h2><img src='{recipe.image}' alt='Image of {recipe.title}' style='width:100px;height:100px;'></div>"
        result_html += '<br><a href="/">Search again</a>'
        return result_html

    api_key = '1f70087e87c54d0a93c39be96d39bdff'
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {'apiKey': api_key, 'ingredients': ','.join(ingredients), 'number': '10'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        recipes = response.json()
        result_html = '<h1>Recipes Found</h1>'
        for recipe_data in recipes:
            new_recipe = Recipe(title=recipe_data['title'], image=recipe_data['image'], cache_key=cache_key)
            db.session.add(new_recipe)
            result_html += f"<div><h2>{recipe_data['title']}</h2><img src='{recipe_data['image']}' alt='Image of {recipe_data['title']}' style='width:100px;height:100px;'></div>"
        db.session.commit()
        result_html += '<br><a href="/">Search again</a>'
        return result_html
    else:
        return jsonify({'error': 'Failed to fetch recipes from API'}), response.status.code

if __name__ == '__main__':
    app.run(debug=True)
