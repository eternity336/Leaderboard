var interval_timer = "";
var tasks = []; // Define tasks variable

function delTable(name){
    $(`#${name}`).empty();
}

function create_player_row(player_name, player_score, tasks) {
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

    // Add total score cell
    var scoreCell = row.insertCell(1);
    scoreCell.innerHTML = player_score;

    // Add task cells
    for (let i = 0; i < tasks.length; i++) {
        let taskCell = row.insertCell(i + 2);  // Task cells start from index 2
        taskCell.id = `task-${player_name}-${i}`;
        taskCell.innerHTML = player_score; // For now, show total score in each task cell
    }
}

function addPlayers(players, tasks) {
    console.log('online', players);
    for (let i = 0; i < players.length; i++) {
        let playerRow = players[i].split(', ');
        create_player_row(playerRow[0], playerRow[1], tasks);  // Use player name and score
    }
}

function refreshData() {
    $.ajax({
        url: "/getdata",
        type: 'GET'
    }).done(function(data) {
        console.log('Received Data:', data);  
        delTable('players');
        tasks = data.data.tasks; // Set the global tasks variable
        addPlayers(data.data.players, tasks);
    });
}

// Initialize the refresh interval
if (interval_timer == ""){
    interval_timer = setInterval(function() {
        refreshData();
    }, 5000)
}
refreshData();
