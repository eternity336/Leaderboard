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
        score_fields = config.get('leaderboard', {}).get('score_fields', [])                                             
        task_max_scores = {task['name']: task.get('max_score', float('inf')) for task in tasks}
except FileNotFoundError:                                                                                                
    print("config.yaml not found. Using default configuration.")                                                         
    tasks = []                                                                                                           
    display_name_field = "name"                                                                                          
    score_fields = []            

print(tasks, display_name_field, score_fields)                                                                                        
@app.route("/")                                                                                                          
def home():                                                                                                              
    ## Homepage for Leaderboard                                                                                          
    return render_template('home.html', players=sorted_list_of_players(), tasks=tasks,                                   
display_name_field=display_name_field)                                                                                   

@app.route("/getdata")                                                                                                   
def get_data():                                                                                                          
    ## Data that is refreshed every sec to homepage                                                                      
    global players                                                                                                       
    data = {                                                                                                             
        'players': sorted_list_of_players(),                                                                             
        'tasks': tasks                                                                                                   
    }                                                                                                                    
    message = {                                                                                                          
            'status' : 200,                                                                                              
            'message' : 'OK',                                                                                            
            'data' : data                                                                                                
            }                                                                                                            
    resp = jsonify(message)                                                                                              
    return resp                                                                                                          

@app.route("/update_players", methods=["POST"])                                                                                  
def update_players():                                                                                                    
    global players                                                                                                       
    print(players)                                                                                                       
    # Get JSON payload                                                                                                   
    new_players = request.get_json()                                                                                     
    print('Incoming JSON Payload:', new_players)                                                                         
    # Validate input                                                                                                     
    if not isinstance(new_players, list):                                                                                
        return jsonify({'error': 'Expected a list of players'}), 400                                                     
    # Process each player in the payload                                                                                 
    for player_data in new_players:                                                                                      
        if display_name_field not in player_data:                                                                        
            continue                                                                                                     
        player_name = player_data[display_name_field]                                                                    
        # Create task scores dictionary                                                                                  
        task_scores = {}                                                                                                 
        total_score = 0                                                                                                  
                                                                                                                         
        for i, task in enumerate(tasks):                                                                                 
            task_name = task['name']                                                                                     
            # Look for score using either direct field match or score_fields mapping                                
            if task_name in player_data:                                                                                 
                score = int(player_data[task_name])                                                                      
            elif len(score_fields) > i and score_fields[i] in player_data:                                               
                score = int(player_data[score_fields[i]])                                                                
            else:                                                                                                        
                score = 0                                                                                                
            
            # Cap the score at maximum allowed value (using weight as max_score)
            max_score = task.get('weight', float('inf'))
            capped_score = min(score, max_score)
            
            # Ensure no negative scores
            capped_score = max(capped_score, 0)
            
            task_scores[task_name] = capped_score                                                                           
            total_score += capped_score  # Changed: sum of scores, not weighted
                                                                                                                         
        print("Tasks Scores:", task_scores)                                                                              
                                                                                                                         
        # Update or add player                                                                                           
        player_found = False                                                                                             
        for i, player in enumerate(players):                                                                             
            if player.startswith(f"{player_name},"):                                                                     
                # Update existing player - store individual scores as comma-separated values                                  
                score_parts = [f"{task_name}:{task_scores[task_name]}" for task_name in task_scores]                      
                players[i] = f"{player_name}, {int(total_score)}, {','.join(score_parts)}"                                
                player_found = True                                                                                      
                break                                                                                                    
                                                                                                                         
        if not player_found:                                                                                             
            # Add new player - store individual scores as comma-separated values                                      
            score_parts = [f"{task_name}:{task_scores[task_name]}" for task_name in task_scores]                      
            players.append(f"{player_name}, {int(total_score)}, {','.join(score_parts)}")                              

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
    # Split the string by comma and return the second part (score)                                                       
    try:                                                                                                                 
        return int(item.split(',')[1])                                                                                   
    except (IndexError, ValueError):                                                                                     
        return 0                                                                                                         

def sorted_list_of_players():                                                                                            
    global players                                                                                                       
    # Parse player data to extract name and score for sorting
    def extract_score(player_str):
        try:
            # Split by comma and get the second element (score)
            parts = player_str.split(', ')
            if len(parts) >= 2:
                return int(parts[1])
            return 0
        except (IndexError, ValueError):
            return 0
    
    return sorted(players, key=extract_score, reverse=True)                                                       

if __name__ == "__main__":                                                                                               
    app.run(debug=True)
