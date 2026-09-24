import os

import requests
from dotenv import load_dotenv

#.envの読み込み
load_dotenv()

#APIの取得
api_key = os.getenv("RIOT_API_KEY")

#API keyをヘッダーへ
headers = {
    "X-Riot-Token": api_key
}

#検索したいRiot ID
game_name = "Nusumaru06"
tag_line = "Ace06"

#アカウントAPIのURL
url = (
    f"https://asia.api.riotgames.com"
    f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
)

#Riot APIにリクエスト
response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print(response.json())

#JSONとしてアカウント情報を取得
account_data = response.json()

#PUUIDを取り出す
puuid = account_data["puuid"]

print("PUUID取得成功!")

#直近20試合分のマッチIDを取得
match_url = (
    f"https://asia.api.riotgames.com"
    f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
)

params = {
    "start": 0,
    "count": 20
}

match_response = requests.get(
    match_url,
    headers=headers,
    params=params
)

print("Match API Status Code:", match_response.status_code)
print(match_response.json())

#Match ID一覧をPythonのリストとして取得
match_ids = match_response.json()

#最も新しいマッチIDを取得
latest_mach_ids = match_ids[0]

print("Latest Match ID:", latest_mach_ids)
