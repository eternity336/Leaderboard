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
        score_fields = [task['name'] for task in tasks]
        font = config.get('leaderboard', {}).get('font', '')
        theme = config.get('leaderboard', {}).get('theme', 'matrix')
except FileNotFoundError:
    print("config.yaml not found. Using default configuration.")
    tasks = []
    display_name_field = "name"
    score_fields = []
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
    for player_data in new_players:
        if display_name_field not in player_data:
            continue
        player_name = player_data[display_name_field]
        task_scores = {}
        total_score = 0
        for i, task in enumerate(tasks):
            task_name = task['name']
            score = 0
            
            # Check if the task name exists in player_data (case-insensitive)
            found_task_key = None
            for key in player_data:
                if key.lower() == task_name.lower():
                    found_task_key = key
                    break
            
            if found_task_key:
                score = int(player_data[found_task_key])
            elif len(score_fields) > i and score_fields[i] in player_data:
                score = int(player_data[score_fields[i]])
            else:
                score = 0

            max_score = task.get('weight', float('inf'))
            capped_score = min(score, max_score)

            capped_score = max(capped_score, 0)

            task_scores[task_name] = capped_score
            total_score += capped_score

        player_found = False
        for i, player in enumerate(players):
            if player.startswith(f"{player_name},"):
                score_parts = [f"{task_name}:{task_scores[task_name]}" for task_name in task_scores]
                players[i] = f"{player_name}, {int(total_score)}, {','.join(score_parts)}"
                player_found = True
                break

        if not player_found:
            score_parts = [f"{task_name}:{task_scores[task_name]}" for task_name in task_scores]
            players.append(f"{player_name}, {int(total_score)}, {','.join(score_parts)}")

    message = {
        'status': 200,
        'message': 'OK',
        'data': sorted_list_of_players()
    }
    resp = jsonify(message)
    return resp

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
