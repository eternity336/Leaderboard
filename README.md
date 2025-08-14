# Simple Leaderboard Server

A simple web application that displays player scores and allows updating player data via HTTP requests.

## Features

- Displays player leaderboard with scores
- Real-time updates through AJAX
- Supports Docker deployment
- Cross-platform compatibility (Linux, Windows)

## Running with Docker

### Prerequisites
- Docker installed on your system

### Steps
1. Build the Docker image:
   ```
   docker build -t simple-leaderboard .
   ```

2. Run the container:
   ```
   docker run -p 5000:5000 simple-leaderboard
   ```

3. Access the leaderboard at `http://localhost:5000`

## Running on Linux

### Prerequisites
- Python 3 installed
- pip installed

### Steps
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application using gunicorn:
   ```
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

3. Access the leaderboard at `http://localhost:5000`

## Running on Windows

### Prerequisites
- Python 3 installed
- pip installed

### Steps
1. Install dependencies:
   ```
   pip install -r requirements_windows.txt
   ```

2. Run the application using waitress:
   ```
   waitress-serve --host=0.0.0.0 --port=5000 app:app
   ```

3. Access the leaderboard at `http://localhost:5000`

## Updating Player Data

To update player data, send a POST request to `/update_players` endpoint with JSON data in the following format:

