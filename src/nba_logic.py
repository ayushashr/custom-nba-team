import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats


def load_player_stats(season="2023-24"):
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed="PerGame"
    )
    df = stats.get_data_frames()[0]

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


def normalize(series: pd.Series) -> pd.Series:
    return (series - series.min()) / (series.max() - series.min()) * 100


def add_strength_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["shooting"] = normalize(df["FG_PCT"] + df["FG3_PCT"])
    df["scoring"] = normalize(df["PTS"])
    df["playmaking"] = normalize(df["AST"])
    df["defense"] = normalize(df["STL"] + df["BLK"])
    df["rebounding"] = normalize(df["REB"])

    return df


def calculate_team_strength(df, player_names):
    found_players = df[df["PLAYER_NAME"].isin(player_names)]

    if len(found_players) != 5:
        raise ValueError("Team must contain exactly 5 players.")

    category_means = found_players[
        ["shooting", "scoring", "playmaking", "defense", "rebounding"]
    ].mean()

    category_means["overall"] = category_means.mean()

    return category_means
