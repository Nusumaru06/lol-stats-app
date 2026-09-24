import os
from pathlib import Path

import requests
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path, override=True)

api_key = os.getenv("RIOT_API_KEY")

print("env path:", env_path)
print("API key exists:", bool(api_key))

if api_key:
    print("Starts with RGAPI-:", api_key.startswith("RGAPI-"))
    print("No extra spaces:", api_key == api_key.strip())

headers = {
    "X-Riot-Token": api_key
}

#puuID取得
def get_puuid(game_name, tag_line):
    url = (
    f"https://asia.api.riotgames.com"
    f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    )
    response = requests.get(url, headers=headers)

    print("Account API Status Code:", response.status_code)
    print(
    "X-Riot-Token sent:",
    "X-Riot-Token" in response.request.headers
    )

    print(
        "Token has value:",
        bool(response.request.headers.get("X-Riot-Token"))
    )

    if response.status_code != 200:
        print(response.json())
        return None

    account_data = response.json()

    return account_data["puuid"]

#matchID取得
def get_match_ids(puuid, count =20):
    match_url = (
        f"https://asia.api.riotgames.com"
        f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
    )

    params = {
        "start": 0,
        "count": count
    }

    response = requests.get(
        match_url,
        headers=headers,
        params=params
    )

    print("Match API Status Code:", response.status_code)

    return response.json()

#テスト
puuid = get_puuid("Nusumaru06", "Ace06")
match_ids = get_match_ids(puuid)
print(puuid)
print(match_ids)