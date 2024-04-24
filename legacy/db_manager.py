import requests
import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "my_project_database"
DB_USER = "my_project_user"
DB_PASSWORD = "your_password"

# Spoonacular API details
API_KEY = '1f70087e87c54d0a93c39be96d39bdff'
SEARCH_URL = 'https://api.spoonacular.com/recipes/complexSearch'

def connect_to_db():
    """
    Establishes connection to the PostgreSQL database and returns the connection object.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except psycopg2.DatabaseError as e:
        print(f"Error connecting to the database: {e}")
    return conn

def insert_recipe(title, image):
    """
    Inserts a new recipe into the recipes table.
    """
    conn = connect_to_db()
    if conn is not None:
        try:
            cur = conn.cursor()
            
            cur.execute("SELECT * FROM recipes WHERE title = %s", (title,))
            result = cur.fetchone()
            
            if result:
                print(f"Recipe '{title}' already exists in the database. Skipping insertion.")
            
            else:
                cur.execute("INSERT INTO recipes (title, image) VALUES (%s, %s)", (title, image))
                conn.commit()
                print("Recipe inserted successfully.")
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error inserting recipe into database: {error}")
        finally:
            if conn is not None:
                cur.close()
                conn.close()

def fetch_and_store_recipes(query, num_recipes):
    """
    Fetches recipes from the Spoonacular API and stores them in the database.
    """
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': num_recipes
    }
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        recipes = response.json().get('results', [])
        for recipe in recipes:
            title = recipe.get('title')
            image = recipe.get('image')
            insert_recipe(title, image)
            
        print(f"{len(recipes)} recipes inserted into the database.")
    else:
        print(f"Failed to fetch recipes: {response.status_code}")

#if __name__ == '__main__':
#    query = 'pasta'
#    fetch_and_store_recipes(query)
