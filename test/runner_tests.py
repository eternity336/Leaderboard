import unittest
import requests
import json
import time
import os
import yaml
from app import app  # Import the Flask application
from app import sorted_list_of_players  # Import the function used in tests

class TestLeaderboardApplication(unittest.TestCase):
    def setUp(self):
        """Start the Flask application for testing."""
        self.app = app.test_client()
        self.app.testing = True
        self.base_url = 'http://localhost:5000'
        self.test_data = [
            {
                "name": "The Matrix Revolution",
                "task 1": 10,
                "task 2": 20,
                "task 3": 30
            },
            {
                "name": "Brute Force",
                "task 1": 5,
                "task 2": 15,
                "task 3": 25
            }
        ]
        self.tasks = [
            {"name": "task 1", "weight": 10},
            {"name": "task 2", "weight": 20},
            {"name": "task 3", "weight": 30}
        ]
        self.config = {
            'leaderboard': {
                'tasks': self.tasks,
                'display_name_field': 'name',
                'font': '',
                'theme': 'matrix'
            }
        }
        # Write test config to file
        with open('config.yaml', 'w') as config_file:
            yaml.safe_dump(self.config, config_file)

    def tearDown(self):
        """Clean up after tests."""
        # Remove test config file
        if os.path.exists('config.yaml'):
            os.remove('config.yaml')

    def test_home_page(self):
        """Test that the home page renders correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        # Check if HTML contains expected elements
        self.assertIn('players', response.data.decode())
        self.assertIn('tasks', response.data.decode())
        self.assertIn('font-family', response.data.decode())
        self.assertIn('theme-selector', response.data.decode())
        self.assertIn('player-table', response.data.decode())

    def test_js_functions_are_loaded(self):
        """Test that JavaScript functions are loaded and available."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        # Check if JavaScript functions are defined
        self.assertIn('create_player_row', response.data.decode())
        self.assertIn('refreshData', response.data.decode())
        self.assertIn('changeFont', response.data.decode())
        self.assertIn('changeTheme', response.data.decode())

    def test_get_data(self):
        """Test that the /getdata endpoint returns correct data."""
        response = self.app.get('/getdata')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('players', data)
        self.assertIn('tasks', data)
        self.assertEqual(len(data['players']), 0)  # No players initially

    def test_update_players(self):
        """Test that updating players works correctly."""
        # First, add some players
        update_data = json.dumps(self.test_data)
        response = self.app.post('/update_players', data=update_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 2)

        # Check if players are correctly calculated
        for player in data['data']:
            player_data = json.loads(player)
            total_score = sum(
                min(int(player_data[f"{task['name'].lower()}"]), task['weight']) 
                for task in self.tasks
            )
            self.assertEqual(player_data['total'], total_score)

    def test_sorted_list_of_players(self):
        """Test the sorted_list_of_players function and DOM rendering."""
        # Add some players
        update_data = json.dumps(self.test_data)
        response = self.app.post('/update_players', data=update_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Check if players are correctly calculated
        for player in data['data']:
            player_data = json.loads(player)
            total_score = sum(
                min(int(player_data[f"{task['name'].lower()}"]), task['weight']) 
                for task in self.tasks
            )
            self.assertEqual(player_data['total'], total_score)

        # Check if DOM reflects the updated player list
        response = self.app.get('/')
        self.assertIn(f"{self.test_data[0]['name']}, {sum(self.test_data[0].values())}, {','.join([f'task {i+1}:{value}' for i, value in enumerate(self.test_data[0].values())])}", response.data.decode())
        self.assertIn(f"{self.test_data[1]['name']}, {sum(self.test_data[1].values())}, {','.join([f'task {i+1}:{value}' for i, value in enumerate(self.test_data[1].values())])}", response.data.decode())

    def test_font_and_theme_application(self):
        """Test that the font and theme are applied correctly."""
        # Set font and theme in config
        self.config['leaderboard']['font'] = 'BoldPixels1.4'
        self.config['leaderboard']['theme'] = 'neon'

        # Write test config to file
        with open('config.yaml', 'w') as config_file:
            yaml.safe_dump(self.config, config_file)

        # Fetch home page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        # Check if font and theme are applied
        self.assertIn('BoldPixels1.4', response.data.decode())
        self.assertIn('neon-theme', response.data.decode())
