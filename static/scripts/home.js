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
                task_scores[
