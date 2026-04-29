import random

def main() -> None:
    player_list: list = [
        "Alice", "bob", "Charlie", "dylan",
        "Emma", "Gregory", "john", "kevin",
        "Liam"
    ]

    print("=== Game Data Alchemist ===\n")
    print(f"Initial list of players: {player_list}")
    players_capitalized: list = [player.capitalize() for player in player_list]
    print(f"New list with all names capitalized: {players_capitalized}")
    capitalized_only: list = [player for player in player_list if player[0].isupper()]
    print(f"New list with capitalized names only: {capitalized_only}")
    score_dict: dict = {player: random.randrange(1000) for player in players_capitalized}
    print(f"Score dict: {score_dict}")
    high_scores: dict = {player: score for player, score in score_dict.items() if score > (sum(score_dict.values()) / len(score_dict))}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()