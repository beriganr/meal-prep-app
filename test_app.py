import unittest
from flask_testing import TestCase
from app import app, db
from models import Recipe
from unittest.mock import patch
import json

class TestFlaskApp(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('requests.get')
    def test_recipe_search_api_call(self, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'id': 123, 'title': 'Pasta with Tomato', 'image': 'url-to-image'}]

        response = self.client.get('/search?ingredients=tomato,pasta')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Pasta with Tomato', str(response.data))

        # Test that the data is cached by checking database entries
        recipes = Recipe.query.all()
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].title, 'Pasta with Tomato')

        # Test subsequent API call uses cache
        response = self.client.get('/search?ingredients=tomato,pasta')
        mock_get.assert_called_once()  # API should not be called again

    def test_invalid_input(self):
        response = self.client.get('/search?ingredients=tomato,pasta,cheese,garlic')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
