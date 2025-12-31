const API_URL = "http://localhost:5000/api";
let selectedPlayers = [];

// Elements
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");
const selectedPlayersDiv = document.getElementById("selectedPlayers");
const playerCount = document.getElementById("playerCount");
const analyzeBtn = document.getElementById("analyzeBtn");

// Search players
searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();
    if (query.length < 2) {
        searchResults.innerHTML = "";
        return;
    }

    const res = await fetch(`${API_URL}/players/search?q=${query}`);
    const data = await res.json();

    if (!data.success) return;

    searchResults.innerHTML = data.players.map(p => `
        <div class="player-item" onclick="addPlayer('${p.PLAYER_NAME}')">
            <div class="player-name">${p.PLAYER_NAME}</div>
        </div>
    `).join("");
});

// Add player
function addPlayer(name) {
    if (selectedPlayers.length >= 5) return alert("Max 5 players");
    if (selectedPlayers.includes(name)) return alert("Already selected");

    selectedPlayers.push(name);
    updateSelectedPlayers();
    searchResults.innerHTML = "";
    searchInput.value = "";
}

// Remove player
function removePlayer(name) {
    selectedPlayers = selectedPlayers.filter(p => p !== name);
    updateSelectedPlayers();
}

// Update UI
function updateSelectedPlayers() {
    playerCount.textContent = selectedPlayers.length;

    if (selectedPlayers.length === 0) {
        selectedPlayersDiv.innerHTML = "<p>No players selected</p>";
        analyzeBtn.disabled = true;
        return;
    }

    selectedPlayersDiv.innerHTML = selectedPlayers.map(p => `
        <div class="selected-player">
            ${p}
            <button onclick="removePlayer('${p}')">Remove</button>
        </div>
    `).join("");

    analyzeBtn.disabled = selectedPlayers.length !== 5;
}

// Analyze team
analyzeBtn.addEventListener("click", async () => {
    const res = await fetch(`${API_URL}/team/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ players: selectedPlayers })
    });

    const data = await res.json();
    if (data.success) displayResults(data.team.team_strengths);
});

// Show results
function displayResults(strengths) {
    const results = document.getElementById("results");
    document.getElementById("resultsCard").style.display = "block";

    results.innerHTML = "";

    Object.entries(strengths).forEach(([category, value]) => {
        const row = document.createElement("div");
        row.className = "strength-row";

        row.innerHTML = `
            <div class="strength-label">
                <span>${capitalize(category)}</span>
                <span>${value.toFixed(1)}</span>
            </div>
            <div class="strength-bar">
                <div 
                    class="strength-fill ${category}" 
                    style="width: ${value}%">
                </div>
            </div>
        `;

        results.appendChild(row);
    });
}

function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1);
}

