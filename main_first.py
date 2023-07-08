"""
Go to Dartcounter website.
Go to the hamburger menu on the left > History > Doubles training > select relevant game.
Press F12 > Select the Network tab.
Look for a document type named as 4 or 5 digits.
Click on it then click on the Headers tab.
This will show the url for the api endpoint for this game.
See images in the project folder.

The python code was initially generated in Postman using the url for a GET request.

"""


import pandas as pd
import requests, json


url = "https://api.dartcounter.net/doubles-trainings/235990"
url2 ="https://api.dartcounter.net/doubles-trainings/40342"
url3 ="https://api.dartcounter.net/doubles-trainings/235792"
url4 ="https://api.dartcounter.net/doubles-trainings/239605"
url5 ="https://api.dartcounter.net/doubles-trainings/240393"
url6 ="https://api.dartcounter.net/doubles-trainings/241939"

def process_get_request(url):

    # df_game = pd.DataFrame(columns=col_list)

    payload = {}
    headers = {
        'Authorization': 'Bearer 1385545|SNU3fmMOReqrR590cSToXuzrDSmMF9aK1Of0o84d',
        'Cookie': '__cflb=02DiuEJarwJfQHRoWfkcFyBvAtpvuGN5ZwecvihxJFXkF'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # initialise the dictionary to store the details for this game
    game_dict= {}

    # print(response.text)
    j = json.loads(response.text)

    id = j["id"]

    game_type = j["settings"]
    print(game_type)

    game_date = j["started_at"]
    print(game_date)


    game_checkout_pc = j["users"][0]["checkout_rate"]
    print(game_checkout_pc)

    # add values to dictionary
    game_dict["id"] = id
    game_dict["game_type"] = game_type
    game_dict["game_date"] = game_date
    game_dict["game_checkout_pc"] = game_checkout_pc

    # for i in range(21):
    #   game_number_01 = j["turns"][i]["number_to_throw"]
    #   # print(game_number_01)
    #
    #   game_throws_01 = j["turns"][i]["darts_thrown"]
    #   # print(game_throws_01)
    #
    #   print(f"Number: {game_number_01} -- Darts thrown: {game_throws_01}")

    for i in range(len(j["turns"])):

        jj = j["turns"][i]

        for key in jj:
            # print(f"Key: {key}")

            if key=="number_to_throw":
                num_value = jj["number_to_throw"]
                # print(f"Number: {num_value}")


            if key=="darts_thrown":
                throw_value = jj["darts_thrown"]
                # print(f"Darts thrown: {throw_value}")

        game_dict[f"Num_{num_value}"] = throw_value

        print(f"Number: {num_value} -- Darts thrown: {throw_value}")

    return game_dict



d1 = process_get_request(url)
d2 = process_get_request(url2)
d3 = process_get_request(url3)
d4 = process_get_request(url4)
d5 = process_get_request(url5)
d6 = process_get_request(url6)

list_of_dicts = [d1,d2,d3,d4,d5,d6]

df = pd.DataFrame(list_of_dicts)

print("x")

df.to_excel("Doubles training.xlsx")

