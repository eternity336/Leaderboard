let interval_timer = "";
let tasks = [];

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

    const playertable = document.getElementById('players');
    const row = playertable.insertRow(-1);
    row.id = `player-${player_name}`;

    const nameCell = row.insertCell(0);
    nameCell.innerHTML = player_name;

    let task_scores = {};
    if (task_scores_str) {
        const score_parts = task_scores_str.split(',');
        for (const part of score_parts) {
            const [task_name, score] = part.split(':');
            if (task_name && score) {
                task_scores[task_name] = parseInt(score);
            }
        }
    }

    for (let i = 0; i < tasks.length; i++) {
        const taskCell = row.insertCell(i + 1);
        taskCell.id = `task-${player_name}-${i}`;
        const task_name = tasks[i].name;
        const max_score = tasks[i].weight || 100;
        const lowercase_task_name = task_name.toLowerCase();

        let score = 0;
        for (const [key, value] of Object.entries(task_scores)) {
            if (key.toLowerCase() === lowercase_task_name) {
                score = parseInt(value);
                break;
            }
        }

        taskCell.innerHTML = `${score}/${max_score}`;
    }

    const scoreCell = row.insertCell(tasks.length + 1);
    scoreCell.innerHTML = player_score;
}

/**
 * Add players to the leaderboard table
 * @param {Array} players - Array of player data strings
 * @param {Array} tasks - Array of task objects
 */
function addPlayers(players, tasks) {
    console.log('online', players);
    
    for (const player of players) {
        const playerRow = player.split(', ');
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
        if (data?.data.tasks) {
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
    // Placeholder function - implement as needed
}

/**
 * Load and apply a theme dynamically
 * @param {string} themeName - Name of the theme to load
 */
function loadTheme(themeName) {
    document.body.classList.remove(...[...document.body.classList].filter(cls => cls.endsWith('-theme')));
    
    if (themeName) {
        document.body.classList.add(themeName + '-theme');
    }
    
    const existingThemes = document.querySelectorAll('link[data-theme]');
    existingThemes.forEach(link => link.remove());
    
    if (themeName) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = `/static/styles/themes/${themeName}.css`;
        link.setAttribute('data-theme', themeName);
        document.head.appendChild(link);
    }
}

/**
 * Load and apply a font dynamically
 * @param {string} fontName - Name of the font to load
 */
function loadFont(fontName) {
    const existingFontStyles = document.querySelectorAll('style[data-font]');
    existingFontStyles.forEach(style => style.remove());
    
    if (fontName) {
        const fontStyle = document.createElement('style');
        fontStyle.id = 'dynamic-font';
        fontStyle.setAttribute('data-font', fontName);
        
        fontStyle.textContent = `
            @font-face {
                font-family: 'ConfigFont';
                src: url('/static/styles/fonts/${fontName}.ttf') format('truetype');
            }
            html, body {
                font-family: 'ConfigFont', sans-serif !important;
            }
        `;
        
        document.head.appendChild(fontStyle);
    }
}

/**
 * Populate font selector with available fonts
 */
function populateFontSelector() {
    $.ajax({
        url: "/getfonts",
        type: 'GET',
        success: function(data) {
            const fontSelect = document.getElementById('font-family');
            // Clear existing options except the default
            fontSelect.innerHTML = '<option value="">Default Font</option>';
            
            if (data?.fonts && Array.isArray(data.fonts)) {
                data.fonts.forEach(font => {
                    const option = document.createElement('option');
                    option.value = font;
                    option.textContent = font.replace('.ttf', '');
                    fontSelect.appendChild(option);
                });
            } else {
                console.error("Invalid fonts data received:", data);
            }
        },
        error: function() {
            console.error("Failed to load fonts");
        }
    });
}

/**
 * Populate theme selector with available themes
 */
function populateThemeSelector() {
    const themeSelect = document.getElementById('theme-selector');
    
    themeSelect.innerHTML = '';
    
    const defaultThemes = [
        { value: 'default', text: 'Default' },
    ];
    
    defaultThemes.forEach(theme => {
        const option = document.createElement('option');
        option.value = theme.value;
        option.textContent = theme.text;
        themeSelect.appendChild(option);
    });
    
    $.ajax({
        url: "/getthemes",
        type: 'GET',
        success: function(data) {
            if (data?.themes && Array.isArray(data.themes)) {
                data.themes.forEach(theme => {
                    const existingThemes = defaultThemes.map(t => t.value);
                    if (!existingThemes.includes(theme)) {
                        const option = document.createElement('option');
                        option.value = theme;
                        option.textContent = theme.charAt(0).toUpperCase() + theme.slice(1);
                        themeSelect.appendChild(option);
                    }
                });
            } else {
                console.error("Invalid themes data received:", data);
            }
        },
        error: function() {
            console.error("Failed to load themes");
        }
    });
}

/**
 * Change font dynamically
 */
function changeFont() {
    const selectedFont = document.getElementById('font-family').value;
    
    if (selectedFont) {
        let fontStyle = document.getElementById('dynamic-font');
        if (!fontStyle) {
            fontStyle = document.createElement('style');
            fontStyle.id = 'dynamic-font';
            document.head.appendChild(fontStyle);
        }
        
        // Load the selected font
        fontStyle.textContent = `
            @font-face {
                font-family: 'SelectedFont';
                src: url('/static/styles/fonts/${selectedFont}') format('truetype');
            }
            html, body {
                font-family: 'SelectedFont', sans-serif !important;
            }
        `;
    } else {
        // Reset to default font
        const fontStyle = document.getElementById('dynamic-font');
        if (fontStyle) {
            fontStyle.remove();
        }
    }
}

/**
 * Change theme dynamically
 */
function changeTheme() {
    const selectedTheme = document.getElementById('theme-selector').value;
    
    // Remove all theme classes except matrix
    document.body.classList.remove(...[...document.body.classList].filter(cls => cls.endsWith('-theme')));
    
    if (selectedTheme) {
        document.body.classList.add(selectedTheme + '-theme');
    }
    
    loadTheme(selectedTheme);
}

/**
 * Toggle sidebar visibility
 */
function toggleSidebar() {
    const fontDropdown = document.querySelector('.font-dropdown');
    const themeDropdown = document.querySelector('.theme-dropdown');
    
    if (fontDropdown.style.opacity === '1') {
        fontDropdown.style.opacity = '0';
        fontDropdown.style.visibility = 'hidden';
        themeDropdown.style.opacity = '0';
        themeDropdown.style.visibility = 'hidden';
    } else {
        fontDropdown.style.opacity = '1';
        fontDropdown.style.visibility = 'visible';
        themeDropdown.style.opacity = '1';
        themeDropdown.style.visibility = 'visible';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('matrix-theme');
    
    // Add click event to the toggle button
    const toggleButton = document.querySelector('.font-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleSidebar);
    }
    
    // Populate font and theme selectors
    populateFontSelector();
    populateThemeSelector();
    
    if (interval_timer === "") {
        interval_timer = setInterval(function() {
            refreshData();
        }, 5000);
    }
    refreshData();
});
