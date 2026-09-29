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

#試合詳細情報取得
def get_match_detail(match_id):
    match_detail_url = (
        f"https://asia.api.riotgames.com"
        f"/lol/match/v5/matches/{match_id}"
    )

    response = requests.get(
    match_detail_url,
    headers=headers
)
    print("Match Detail Status Code:", response.status_code)

    return response.json()

# 1試合のデータから指定プレイヤーの成績を取り出す
def get_player_data(match_data, puuid):

    participants = match_data["info"]["participants"]

    for participant in participants:
        if participant["puuid"] == puuid:
            return {
                #試合基本情報
                "match_id": match_data["matadata"]["matchID"],
                "summoner_name": (
                    participant["riotIdGameName"]
                    + "#"
                    +participant["riotIdTagline"]
                ),
                "champion": participant["championName"],
                "lane": participant["lane"],
                "win": "win" if participant["win"] else "lose",
                "Match duration": match_data["info"]["gameDuration"],
                #スタッツ
                "kills": participant["kills"],
                "deaths": participant["deaths"],
                "assists": participant["assists"],
                "Kda": participant["challenges"].get("kda",None),
                "Kill participation rate": participant["challenge"].get("killParticipation", None),
                #ダメージとゴールド
                "total damage to champions": participant["totalDamageDealtToChampions"],
                "total gold acquired": participant["goldEarned"],
                "damage per minute": participant["challenges"].get("damagePerMinute", None),
                "gold per minute": participant["challenges"].get("goldPerMinute", None),
            }

    return None

#テスト
puuid = get_puuid("Nusumaru06", "Ace06")

if puuid is not None:
    match_ids = get_match_ids(puuid)

    latest_match_ids = match_ids[0]

    match_data = get_match_detail(latest_match_ids)

    print(match_data)
