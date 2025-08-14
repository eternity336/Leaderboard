var interval_timer = "";
var tasks = [];

/**
 * Delete all rows from a table
 * @param {string} name - The ID of the table to clear
 */
function delTable(name){
    $(`#${name}`).empty();
}

/**
 * Create a row for a player in the leaderboard table
 * @param {string} player_name - Name of the player
 * @param {string} player_score - Total score of the player
 * @param {Array} tasks - Array of task objects
 * @param {string} task_scores_str - Comma-separated string of task scores
 */
function create_player_row(player_name, player_score, tasks, task_scores_str) {
    if (!tasks || !Array.isArray(tasks)) {
        console.error("Tasks array is not defined or invalid");
        return;
    }

    var playertable = document.getElementById('players');
    var row = playertable.insertRow(-1);
    row.id = `player-${player_name}`;

    var nameCell = row.insertCell(0);
    nameCell.innerHTML = player_name;

    let task_scores = {};
    if (task_scores_str) {
        let score_parts = task_scores_str.split(',');
        for (let part of score_parts) {
            let [task_name, score] = part.split(':');
            if (task_name && score) {
                task_scores[task_name] = parseInt(score);
            }
        }
    }

    for (let i = 0; i < tasks.length; i++) {
        let taskCell = row.insertCell(i + 1);
        taskCell.id = `task-${player_name}-${i}`;
        let task_name = tasks[i].name;
        if (task_scores[task_name] !== undefined) {
            taskCell.innerHTML = task_scores[task_name];
        } else {
            taskCell.innerHTML = "0";
        }
    }

    var scoreCell = row.insertCell(tasks.length + 1);
    scoreCell.innerHTML = player_score;
}

/**
 * Add players to the leaderboard table
 * @param {Array} players - Array of player data strings
 * @param {Array} tasks - Array of task objects
 */
function addPlayers(players, tasks) {
    console.log('online', players);
    for (let i = 0; i < players.length; i++) {
        let playerRow = players[i].split(', ');
        create_player_row(playerRow[0], playerRow[1], tasks, playerRow.slice(2).join(', '));
    }
}

/**
 * Refresh leaderboard data from the server
 */
function refreshData() {
    $.ajax({
        url: "/getdata",
        type: 'GET'
    }).done(function(data) {
        console.log('Received Data:', data);  
        delTable('players');
        if (data.data && data.data.tasks) {
            tasks = data.data.tasks;
        }
        addPlayers(data.data.players, tasks);
        
        updateTaskScores();
    }).fail(function(xhr, status, error) {
        console.error('Failed to fetch data:', error);
    });
}

/**
 * Update task scores (placeholder function)
 */
function updateTaskScores() {
}

if (interval_timer == ""){
    interval_timer = setInterval(function() {
        refreshData();
    }, 5000)
}
refreshData();
