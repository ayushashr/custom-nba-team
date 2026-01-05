from flask import Flask, request, jsonify
from flask_cors import CORS
from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd

app = Flask(__name__)
CORS(app)

print("Loading NBA player stats...")
df = leaguedashplayerstats.LeagueDashPlayerStats(
    season="2023-24",
    per_mode_detailed="PerGame"
).get_data_frames()[0]

df = df[["PLAYER_NAME", "PTS","REB","AST","STL","BLK","FG_PCT","FG3_PCT",]
]


# -----------------------
# Player Search
# -----------------------
@app.route("/players/search")
def search_players():
    q = request.args.get("q", "").lower()
    matches = df[df["PLAYER_NAME"].str.lower().str.contains(q)]

    players = matches.head(10).to_dict(orient="records")
    return jsonify({"success": True, "players": players})


# -----------------------
# Team Analysis
# -----------------------
@app.route("/team/analyze", methods=["POST"])
def analyze_team():
    data = request.get_json()
    names = data.get("players", [])

    if len(names) != 5:
        return jsonify({"success": False, "error": "Team must have exactly 5 players"})

    team = df[df["PLAYER_NAME"].isin(names)]

    def scale(value, max_value):
        return min((value / max_value) * 100, 100)

    strengths = {
        "scoring": scale(team["PTS"].mean(), 30),
        "rebounding": scale(team["REB"].mean(), 15),
        "playmaking": scale(team["AST"].mean(), 10),
        "shooting": scale(
            team["FG_PCT"].mean() + team["FG3_PCT"].mean(),
            1.0
        ),
        "defense": scale(
            team["STL"].mean() + team["BLK"].mean(),
            5
        ),
    }



    strengths["overall"] = sum(strengths.values()) / len(strengths)

    return jsonify({
        "success": True,
        "team_strengths": strengths
    })


if __name__ == "__main__":
    app.run(debug=True)
