from flask import Flask, jsonify, request
from flask_cors import CORS

from nba_logic import (
    load_player_stats,
    add_strength_metrics,
    calculate_team_strength,
)

app = Flask(__name__)
CORS(app)

print("Loading NBA data...")
df = load_player_stats()
df = add_strength_metrics(df)
print("NBA data loaded.")


@app.route("/api/players/search")
def search_players():
    query = request.args.get("q", "").lower()

    if len(query) < 2:
        return jsonify({"success": True, "players": []})

    matches = df[df["PLAYER_NAME"].str.lower().str.contains(query)]

    players = matches.head(20)[
        ["PLAYER_NAME", "PTS", "REB", "AST"]
    ].to_dict(orient="records")

    return jsonify({
        "success": True,
        "players": players
    })


@app.route("/api/team/analyze", methods=["POST"])
def analyze_team():
    data = request.get_json()
    player_names = data.get("players", [])

    try:
        strengths = calculate_team_strength(df, player_names)

        return jsonify({
            "success": True,
            "team": {
                "team_strengths": strengths.to_dict()
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
