import unittest
from app import app, db, Recipe
from unittest.mock import patch

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search for Recipes', response.data)

    def test_valid_search(self):
        response = self.app.get('/search?ingredient1=chicken&diet=gluten-free')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Recipes Found', response.data)

    def test_no_ingredients(self):
        response = self.app.get('/search?ingredient1=&ingredient2=&ingredient3=')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
