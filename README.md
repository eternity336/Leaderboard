# Simple Leaderboard Server

A simple web application that displays player scores and allows updating player data via HTTP requests.

## Features

- Displays player leaderboard with scores
- Real-time updates through AJAX
- Supports Docker deployment
- Cross-platform compatibility (Linux, Windows)

## Running with Docker Compose

### Prerequisites
- Docker and Docker Compose installed on your system

### Steps
1. Run the application using Docker Compose:
   ```
   docker-compose up
   ```

2. Access the leaderboard at `http://localhost:5000`

3. To run in detached mode:
   ```
   docker-compose up -d
   ```

4. To stop the containers:
   ```
   docker-compose down
   ```

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

