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
