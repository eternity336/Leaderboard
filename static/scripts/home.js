var interval_timer = "";
var tasks = []; // Define tasks variable

function delTable(name){
    $(`#${name}`).empty();
}

function create_player_row(player_name, player_score, tasks, task_scores_str) {
    if (!tasks || !Array.isArray(tasks)) {
        console.error("Tasks array is not defined or invalid");
        return;
    }

    var playertable = document.getElementById('players');
    var row = playertable.insertRow(-1);
    row.id = `player-${player_name}`;

    // Add player name cell
    var nameCell = row.insertCell(0);
    nameCell.innerHTML = player_name;

    // Parse task scores from string
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

    // Add task cells (skip first column for name)
    for (let i = 0; i < tasks.length; i++) {
        let taskCell = row.insertCell(i + 1);  // Task cells start from index 1
        taskCell.id = `task-${player_name}-${i}`;
        let task_name = tasks[i].name;
        if (task_scores[task_name] !== undefined) {
            taskCell.innerHTML = task_scores[task_name];
        } else {
            taskCell.innerHTML = "0";
        }
    }

    // Add total score cell at the end
    var scoreCell = row.insertCell(tasks.length + 1);
    scoreCell.innerHTML = player_score;
}

function addPlayers(players, tasks) {
    console.log('online', players);
    for (let i = 0; i < players.length; i++) {
        let playerRow = players[i].split(', ');
        create_player_row(playerRow[0], playerRow[1], tasks, playerRow.slice(2).join(', '));  // Pass task scores
    }
}

function refreshData() {
    $.ajax({
        url: "/getdata",
        type: 'GET'
    }).done(function(data) {
        console.log('Received Data:', data);  
        delTable('players');
        if (data.data && data.data.tasks) {
            tasks = data.data.tasks; // Set the global tasks variable
        }
        addPlayers(data.data.players, tasks);
        
        // Update task scores for each player
        updateTaskScores();
    }).fail(function(xhr, status, error) {
        console.error('Failed to fetch data:', error);
    });
}

function updateTaskScores() {
    // This function would normally make additional calls to get detailed player data
    // For now, we'll just keep the placeholder values
    // In a real implementation, you'd need to:
    // 1. Make separate API calls for each player to get their task scores
    // 2. Parse and update the task cells accordingly
    
    // Since we're not implementing the detailed data retrieval in this simple example,
    // we'll just leave the placeholder values as they are
}

// Initialize the refresh interval
if (interval_timer == ""){
    interval_timer = setInterval(function() {
        refreshData();
    }, 5000)
}
refreshData();
