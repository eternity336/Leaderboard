import yaml
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
players = []

try:
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        tasks = config.get('leaderboard', {}).get('tasks', [])
        display_name_field = "name"
        font = config.get('leaderboard', {}).get('font', '')
        theme = config.get('leaderboard', {}).get('theme', 'matrix')
except FileNotFoundError:
    print("config.yaml not found. Using default configuration.")
    tasks = []
    display_name_field = "name"
    font = ''
    theme = 'matrix'


@app.route("/")
def home():
    """Render the home page with leaderboard data.

    Returns:
        Rendered HTML template with players, tasks, display name field, font and theme
    """
    return render_template('home.html', players=sorted_list_of_players(), tasks=tasks,
                            display_name_field=display_name_field, font=font, theme=theme)


@app.route("/getdata")
def get_data():
    """Get current leaderboard data.

    Returns:
        JSON response containing players and tasks data
    """
    global players
    data = {
        'players': sorted_list_of_players(),
        'tasks': tasks
    }
    message = {
        'status': 200,
        'message': 'OK',
        'data': data
    }
    resp = jsonify(message)
    return resp


@app.route("/getfonts")
def get_fonts():
    """Get list of available fonts from the fonts directory.

    Returns:
        JSON response containing list of font files
    """
    fonts_dir = 'static/styles/fonts'
    try:
        if os.path.exists(fonts_dir):
            fonts = [f for f in os.listdir(fonts_dir) if f.endswith(('.ttf', '.otf'))]
            return jsonify({'fonts': fonts})
        else:
            return jsonify({'fonts': []})
    except Exception as e:
        print(f"Error reading fonts directory: {e}")
        return jsonify({'fonts': []})


@app.route("/getthemes")
def get_themes():
    """Get list of available themes from the themes directory.

    Returns:
        JSON response containing list of theme files
    """
    themes_dir = 'static/styles/themes'
    try:
        if os.path.exists(themes_dir):
            # Get all CSS files in the themes directory
            themes = [f for f in os.listdir(themes_dir) if f.endswith('.css') and f != 'styles.css']
            # Remove .css extension from filenames for display
            theme_names = [os.path.splitext(theme)[0] for theme in themes]
            return jsonify({'themes': theme_names})
        else:
            return jsonify({'themes': []})
    except Exception as e:
        print(f"Error reading themes directory: {e}")
        return jsonify({'themes': []})


@app.route("/update_players", methods=["POST"])
def update_players():
    """Update player scores from POST request.

    Returns:
        JSON response with updated leaderboard data
    """
    global players
    new_players = request.get_json()
    if not isinstance(new_players, list):
        return jsonify({'error': 'Expected a list of players'}), 400

    updated_players = []

    for player_data in new_players:
        parsed_player = parse_player_data(player_data)
        if not parsed_player:
            continue

        player_name, task_scores = parsed_player
        total_score = sum(calculate_task_score(task, task_scores) for task in tasks)

        if update_player_in_list(players, player_name, task_scores):
            updated_players.extend(players)
        else:
            added_player = add_new_player(player_name, task_scores, total_score)
            updated_players.extend(players)
            updated_players.append(added_player)

    message = {
        'status': 200,
        'message': 'OK',
        'data': sorted_list_of_players()
    }
    resp = jsonify(message)
    return resp


def parse_player_data(player_data):
    """Extract player name and task scores from player data.

    Args:
        player_data (dict): Player data from the request.

    Returns:
        tuple: (player_name, task_scores) or None if invalid.
    """
    if display_name_field not in player_data:
        return None

    player_name = player_data[display_name_field]
    task_scores = {}

    for task in tasks:
        task_name = task['name'].lower()  # Normalize task name to lowercase
        score = 0

        # Check for exact match first (case-insensitive)
        if task_name in player_data:
            score = int(player_data[task_name])

        max_score = task.get('weight', float('inf'))
        capped_score = min(score, max_score)
        capped_score = max(capped_score, 0)

        task_scores[task_name] = capped_score

    return player_name, task_scores


def calculate_task_score(task, task_scores):
    """Calculate the capped score for a task.

    Args:
        task (dict): Task definition.
        task_scores (dict): Player's task scores.

    Returns:
        int: Capped score for the task.
    """
    task_name = task['name']
    score = task_scores.get(task_name, 0)
    max_score = task.get('weight', float('inf'))
    return min(max(score, 0), max_score)


def update_player_in_list(players, player_name, task_scores):
    """Update an existing player in the list.

    Args:
        players (list): List of players.
        player_name (str): Player name.
        task_scores (dict): Task scores.

    Returns:
        bool: True if player was found and updated, False otherwise.
    """
    for player in players:
        # Convert both to lowercase for case-insensitive comparison
        if player.lower().startswith(f"{player_name.lower()},"):
            score_parts = [f"{task_name}:{task_scores[task_name]}" for task_name in task_scores]
            # Update the player string in the list
            index = players.index(player)
            players[index] = f"{player_name}, {sum(task_scores.values())}, {','.join(score_parts)}"
            return True
    return False


def add_new_player(player_name, task_scores, total_score):
    """Add a new player to the list.

    Args:
        player_name (str): Player name.
        task_scores (dict): Task scores.
        total_score (int): Total score.

    Returns:
        str: Formatted player string.
    """
    score_parts = [f"{task_name}:{task_scores[task_name]}" for task_name in task_scores]
    return f"{player_name}, {total_score}, {','.join(score_parts)}"


def extract_second_value(item):
    """Extract the second value from a comma-separated string.

    Args:
        item (str): Comma-separated string

    Returns:
        int: The second value parsed as integer, or 0 if parsing fails
    """
    try:
        return int(item.split(',')[1])
    except (IndexError, ValueError):
        return 0


def sorted_list_of_players():
    """Sort players by their scores in descending order.

    Returns:
        list: Sorted list of players based on scores
    """
    global players
    def extract_score(player_str):
        try:
            parts = player_str.split(', ')
            if len(parts) >= 2:
                return int(parts[1])
            return 0
        except (IndexError, ValueError):
            return 0

    return sorted(players, key=extract_score, reverse=True)


if __name__ == "__main__":
    app.run(debug=True)
