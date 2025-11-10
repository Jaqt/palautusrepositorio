import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []
    preferred_nationality = "FIN"

    for player_dict in response:
        player = Player(player_dict)
        if player.nationality == preferred_nationality:
            players.append(player)

    print(f"Players from {preferred_nationality}:")

    for player in players:
        print(player)

if __name__ == "__main__":
    main()
