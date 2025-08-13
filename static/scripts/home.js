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

    // Add task cells (skip first two columns for name and total)
    for (let i = 0; i < tasks.length; i++) {
        let taskCell = row.insertCell(i + 1);  // Task cells start from index 1
        taskCell.id = `task-${player_name}-${i}`;
        taskCell.innerHTML = "0"; // Initialize with 0, will be updated by backend data
    }

    // Add total score cell at the end
    var scoreCell = row.insertCell(tasks.length + 1);
    scoreCell.innerHTML = player_score;
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
        if (data.data && data.data.tasks) {
            tasks = data.data.tasks; // Set the global tasks variable
        }
        addPlayers(data.data.players, tasks);
    }).fail(function(xhr, status, error) {
        console.error('Failed to fetch data:', error);
    });
}

// Initialize the refresh interval
if (interval_timer == ""){
    interval_timer = setInterval(function() {
        refreshData();
    }, 5000)
}
refreshData();
