from flask import Flask, render_template, jsonify
from flask import request

app = Flask(__name__)

players = []

@app.route("/")
def home():
    ## Homepage for Leaderboard 
    return render_template('home.html', players=sorted_list_of_players())

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
    players = request.get_json()
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
