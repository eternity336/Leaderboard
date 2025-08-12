import yaml
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

players = []

# Load configuration from YAML file
try:
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
        tasks = config.get('leaderboard', {}).get('tasks', [])
        display_name_field = config.get('leaderboard', {}).get('display_name_field', "name")
        score_fields = config.get('leaderboard', {}).get('score_fields', ["task_1", "task_2", "task_3"])
except FileNotFoundError:
    print("config.yaml not found. Using default configuration.")
    tasks = [{"name": "Task 1", "weight": 20}, {"name": "Task 2", "weight": 30}, {"name": "Task 3", "weight": 50}]
    display_name_field = "name"
    score_fields = ["task_1", "task_2", "task_3"]

@app.route("/")
def home():
    ## Homepage for Leaderboard 
    return render_template('home.html', players=sorted_list_of_players(), tasks=tasks, display_name_field=display_name_field)

@app.route("/getdata")
def get_data():
    ## Data that is refreshed every sec to homepage
    global players
    data = {
        'players': sorted_list_of_players(), 
    }
    message = {
            'status' : 200,
            'message' : 'OK',
            'data' : data
            }
    resp = jsonify(message)
    return resp

@app.route("/update_players", methods=['POST'])
def update_players():
    global players
    print(players)
    
    # Print the incoming JSON payload for debugging
    new_players = request.get_json()
    print('Incoming JSON Payload:', new_players)

    # Validate and convert input data
    for player in new_players:
        if display_name_field not in player or any(field not in player for field in score_fields):
            continue
        
        player_id = player[display_name_field]
        
        task_scores = {}
        for task, field in zip(tasks, score_fields):
            task_score = int(player.get(field, 0))  # Get the score from player dictionary
            if task_score > 0:
                task_scores[task['name']] = task_score
        
        # Convert task scores to integers and calculate total score
        player_score = sum(task_scores.get(task['name'], 0) * task['weight'] / 100 for task in tasks)
        
        players.append(f"{player_id}, {int(player_score)}")

    print(players)
    message = {
            'status' : 200,
            'message' : 'OK',
            'data' : sorted_list_of_players()
            }
    resp = jsonify(message)
    return resp

# Define a function to extract the second value from each string
def extract_second_value(item):
    # Split the string by comma and return the second part
    return int(item.split(',')[1])

def sorted_list_of_players():
    global players
    return sorted(players, key=extract_second_value, reverse=True)

if __name__ == "__main__":
    app.run(debug=True)