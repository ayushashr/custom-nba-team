import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

def load_player_stats(season="2023-24"):
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame"
    )
    df = stats.get_data_frames()[0]

    # Keep only relevant columns
    df = df[
        [
            "PLAYER_NAME",
            "PTS",
            "AST",
            "REB",
            "STL",
            "BLK",
            "FG_PCT",
            "FG3_PCT",
        ]
    ]

    return df

# min-max normalization to scale stats between 0 and 100 in order to compare players
# for example, points (0-30 range) and steals (0-3 range) become comparable.
def normalize(series: pd.Series) -> pd.Series:
    """Min-max normalize a pandas Series to 0–100."""
    return (series - series.min()) / (series.max() - series.min()) * 100


def add_strength_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["shooting"] = normalize(df["FG_PCT"] + df["FG3_PCT"])
    df["scoring"] = normalize(df["PTS"])
    df["playmaking"] = normalize(df["AST"])
    df["defense"] = normalize(df["STL"] + df["BLK"])
    df["rebounding"] = normalize(df["REB"])

    return df

# calculate team strength based on averaged player metrics
def calculate_team_strength(df, player_names):
    found_players = df[df["PLAYER_NAME"].isin(player_names)]
    found_names = set(found_players["PLAYER_NAME"])
    requested_names = set(player_names)

    missing = requested_names - found_names

    if missing:
        raise ValueError(
            f"The following players were not found in the dataset: {missing}"
        )

    if len(found_players) != 5:
        raise ValueError(
            f"Expected 5 players, found {len(found_players)}."
        )

    category_means = found_players[
        ["shooting", "scoring", "playmaking", "defense", "rebounding"]
    ].mean()

    category_means["overall"] = category_means.mean()

    return category_means

def main():
    print("Loading NBA player stats...")
    df = load_player_stats()

    print("Calculating strength metrics...")
    df = add_strength_metrics(df)

    # Example team
    team = [
        "Stephen Curry",
        "LeBron James",
        "Kevin Durant",
        "Kawhi Leonard",
        "Giannis Antetokounmpo",
    ]

    print("\nCalculating team strength for:")
    for player in team:
        print("-", player)

    scores = calculate_team_strength(df, team)

    print("\nTeam Strength Scores (0–100):")
    print(scores.round(2))


if __name__ == "__main__":
    main()
