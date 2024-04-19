import unittest
from flask_testing import TestCase
from app import app  # Import the Flask app

class TestFlaskApi(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_recipe_search(self):
        response = self.client.get('/search?ingredient=pasta')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pasta', response.json[0]['title'].lower())  # Assuming the title contains the ingredient

if __name__ == '__main__':
    unittest.main()

