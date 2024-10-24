var interval_timer = "";

function delTable(name){
    $(`#${name}`).empty();
}

function create_player_row(player, online){
    player = player.split(', ');
    var playertable = document.getElementById('players');
    var row = playertable.insertRow(-1);
    var namecell = row.insertCell(0);
    var playerscore = row.insertCell(1);
    namecell.innerHTML = player[0];
    playerscore.innerHTML = player[1];
}

function addPlayers(players, online){
    console.log('online', players)
    for (let i = 0; i < players.length; i++){
        create_player_row(players[i])
    }
}

function refreshData(){
    $.ajax({
                url: "/getdata",
                type: 'GET'
            }).done(function(data){
                console.log(data);
                delTable('players');
                addPlayers(data.data.players);
            });
}

if (interval_timer == ""){
    interval_timer = setInterval(function() {
        refreshData();
    }, 5000)
}
refreshData();