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
            {"name": "task 2", "weight": 2
