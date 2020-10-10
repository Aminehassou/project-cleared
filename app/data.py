from config import Config
from flask import url_for
import requests
import json

def get_games(query):
    l = {"suggestions": []}
    r = requests.post("https://api.igdb.com/v4/games",  
                headers = {"Client-ID": Config.CLIENT_ID, "Authorization": "Bearer {}".format(Config.API_AUTH)}, data = 'fields name, platforms.name, cover.image_id; where name ~ *"{}"* & rating != null; sort rating desc; limit 10;'.format(query))
    request = r.json()
    
    
    for item in request:
        l["suggestions"].append({"value": item["name"], "data": item["id"]})
    return l

def get_game_by_id(id):
    r = requests.post("https://api.igdb.com/v4/games",  
                headers = {"Client-ID": Config.CLIENT_ID, "Authorization": "Bearer {}".format(Config.API_AUTH)}, data = 'fields name, involved_companies.developer, involved_companies.publisher, involved_companies.company.name, platforms.name, cover.image_id, first_release_date; where id = {}; limit 1;'.format(id))
    return r.json()[0]
