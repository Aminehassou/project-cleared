from config import Config
from flask import url_for
import requests
import json

def get_games(query):
    l = []
    r = requests.post("https://api.igdb.com/v4/games",  
                headers = {"Client-ID": Config.CLIENT_ID, "Authorization": "Bearer {}".format(Config.API_AUTH)}, data = 'fields name, platforms.name, cover.image_id; where name ~ *"{}"* & rating != null; sort rating desc; limit 10;'.format(query))
    request = r.json()
    for item in request:
        print(item)
        if "cover" not in item:
            item["cover"] = {"image_id": None}
        l.append({"name": item["name"], "id": item["id"], "image_id": item["cover"]["image_id"]})
    return l

def get_game_by_id(id):
    r = requests.post("https://api.igdb.com/v4/games",  
                headers = {"Client-ID": Config.CLIENT_ID, "Authorization": "Bearer {}".format(Config.API_AUTH)}, data = 'fields name, summary, involved_companies.developer, involved_companies.publisher, involved_companies.company.name, platforms.name, cover.image_id, similar_games.name, first_release_date; where id = {}; limit 1;'.format(id))
    return r.json()[0]
