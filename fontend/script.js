const API_URL = "http://localhost:5000";

let selectedPlayers = [];

const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");
const selectedPlayersDiv = document.getElementById("selectedPlayers");
const playerCount = document.getElementById("playerCount");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultsCard = document.getElementById("resultsCard");
const resultsDiv = document.getElementById("results");

/* -----------------------
   Player Search
------------------------ */
searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();

    if (query.length < 2) {
        searchResults.innerHTML = "";
        return;
    }

    const response = await fetch(`${API_URL}/players/search?q=${query}`);
    const data = await response.json();

    searchResults.innerHTML = "";

    data.players.forEach(player => {
        const div = document.createElement("div");
        div.className = "player-item";
        div.textContent = player.PLAYER_NAME;
        div.onclick = () => addPlayer(player.PLAYER_NAME);
        searchResults.appendChild(div);
    });
});

/* -----------------------
   Add / Remove Players
------------------------ */
function addPlayer(name) {
    if (selectedPlayers.length >= 5) return;
    if (selectedPlayers.includes(name)) return;

    selectedPlayers.push(name);
    updateSelectedPlayers();
    searchResults.innerHTML = "";
    searchInput.value = "";
}

function removePlayer(name) {
    selectedPlayers = selectedPlayers.filter(p => p !== name);
    updateSelectedPlayers();
}

function updateSelectedPlayers() {
    selectedPlayersDiv.innerHTML = "";

    selectedPlayers.forEach(player => {
        const div = document.createElement("div");
        div.className = "selected-player";
        div.innerHTML = `
            <span>${player}</span>
            <button onclick="removePlayer('${player}')">Remove</button>
        `;
        selectedPlayersDiv.appendChild(div);
    });

    playerCount.textContent = selectedPlayers.length;
    analyzeBtn.disabled = selectedPlayers.length !== 5;
    resultsCard.style.display = "none";
}

/* -----------------------
   Analyze Team
------------------------ */
analyzeBtn.addEventListener("click", async () => {
    const response = await fetch(`${API_URL}/team/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ players: selectedPlayers })
    });

    const data = await response.json();
    displayResults(data.team_strengths);
});

/* -----------------------
   Display Strength Bars
------------------------ */
function displayResults(strengths) {
    resultsDiv.innerHTML = "";

    Object.entries(strengths).forEach(([category, value]) => {
        const row = document.createElement("div");
        row.className = "strength-row";

        row.innerHTML = `
            <div class="strength-label">
                <span>${capitalize(category)}</span>
                <span>${value.toFixed(1)}/100</span>
            </div>
            <div class="strength-bar">
                <div class="strength-fill ${category}" style="width:${value}%"></div>
            </div>
        `;

        resultsDiv.appendChild(row);
    });

    resultsCard.style.display = "block";
}

/* -----------------------
   Utility
------------------------ */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
