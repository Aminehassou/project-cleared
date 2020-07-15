import config
import requests
import json

settings = {"fields": ["name, platforms"]}

r = requests.get("https://api-v3.igdb.com/games/",  headers = {"user-key": config.KEY}, data = "fields name, platforms.name, first_release_date	; limit 100;")
games = r.json()
for game in games:
    print(game)

