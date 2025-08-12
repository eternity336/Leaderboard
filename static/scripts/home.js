var interval_timer = "";

function delTable(name){
    $(`#${name}`).empty();
}

function create_player_row(player, tasks) {
    if (!tasks || !Array.isArray(tasks)) {
        console.error("Tasks array is not defined or invalid");
        return;
    }

    var playertable = document.getElementById('players');
    var row = playertable.insertRow(-1);
    row.id = `player-${player}`;

    // Add other cells as needed

    for (let i = 0; i < tasks.length; i++) {
        let taskCell = row.insertCell(i + 2);  // Assuming player name and total score take up the first two cells
        taskCell.id = `task-${i}`;
    }
}

function addPlayers(players, tasks) {
    console.log('online', players);
    for (let i = 0; i < players.length; i++) {
        let playerRow = players[i].split(', ');
        create_player_row(playerRow[0], tasks);  // Use player name as the identifier
        addScoreCells(playerRow[1], tasks);
    }
}

function addScoreCells(score, tasks) {
    if (!tasks || !Array.isArray(tasks)) {
        console.error("Tasks array is not defined or invalid");
        return;
    }

    let scoreValues = JSON.parse(score).score;  // Assuming score is in JSON format
    for (let i = 0; i < tasks.length; i++) {
        let taskCell = document.getElementById(`task-${i}`);
        if (taskCell) {
            taskCell.innerHTML = scoreValues[i];
        } else {
            console.error(`Task cell with id 'task-${i}' not found`);
        }
    }
}

function refreshData() {
    $.ajax({
        url: "/getdata",
        type: 'GET'
    }).done(function(data) {
        console.log('Received Data:', data);  
        delTable('players');
        addPlayers(data.data.players, tasks);
    });
}

if (interval_timer == ""){
    interval_timer = setInterval(function() {
        refreshData();
    }, 5000)
}
refreshData();