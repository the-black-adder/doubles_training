"""
File for testing responses from API calls.
"""

import requests, json

def process_get_request_matches(game):

    url = f"https://api.dartcounter.net/matches/{game}"

    payload = {}
    headers = {
        'Authorization': 'Bearer 1385545|SNU3fmMOReqrR590cSToXuzrDSmMF9aK1Of0o84d',
        'Cookie': '__cflb=02DiuEJarwJfQHRoWfkbiCSQA2QMWVqeBPDNwKH8LyaAf'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:

        # initialise the dictionary to store the details for this game
        game_dict= {}

        # print(response.text)
        j = json.loads(response.text)
        stats = j["users"][0]

        return j

match1 = "26811943"
p = process_get_request_matches(match1)

x=0