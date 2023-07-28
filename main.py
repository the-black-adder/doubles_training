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
import streamlit as st


def process_get_request(game):

    # df_game = pd.DataFrame(columns=col_list)

    url = f"https://api.dartcounter.net/doubles-trainings/{game}"

    payload = {}
    headers = {
        'Authorization': 'Bearer 1385545|SNU3fmMOReqrR590cSToXuzrDSmMF9aK1Of0o84d',
        'Cookie': '__cflb=02DiuEJarwJfQHRoWfkcFyBvAtpvuGN5ZwecvihxJFXkF'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:

        # initialise the dictionary to store the details for this game
        game_dict= {}

        # print(response.text)
        j = json.loads(response.text)

        id = j["id"]

        game_type = j["settings"]
        # print(game_type)

        game_date = j["started_at"]
        # print(game_date)


        game_checkout_pc = j["users"][0]["checkout_rate"]
        # print(game_checkout_pc)

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

            # print(f"Number: {num_value} -- Darts thrown: {throw_value}")

        return game_dict

    else:
        print(f"ERROR: Response code = {response.status_code}")
        return "error"


# initialise empty list
list_of_dicts = []

games = [
235990,
40342,
235792,
239605,
240393,
241939,
    246077,
    248429
]

for game in games:
    xdict = process_get_request(game)

    if type(xdict) is dict:

        # aim to build up a list of dictionaries to create the data frame from
        # faster than appending a dictionary to a dataframe in a loop
        # e.g. list_of_dicts = [d1,d2,d3,d4,d5,d6]

        list_of_dicts.append(xdict)
    else:
        print(f"SKIPPING {game}. DICTIONARY NOT RETURNED.")

df_games = pd.DataFrame(list_of_dicts)


df_games.to_excel("Doubles training.xlsx",index=False)

# --- Prepare data frames for use with streamlit

# 1. Add a column totalling all the darts thrown in that session
cols_to_sum = [n for n in list(df_games) if n.lower().startswith("num")]

df_games['total_darts'] = df_games[cols_to_sum].sum(axis=1)

# 2. Create a data frame of averages
av_dict = {}
for a in cols_to_sum:
    av_dict[a.replace("Num_","")] = [float("{:,.1f}".format(df_games[a].mean())),float("{:,.1f}".format(df_games[a].std()))]

df_avg = pd.DataFrame(av_dict)
# index=['Average number of darts']

df_avg2 = df_avg.transpose()

# Changing column names with index number
mapping = {df_avg2.columns[0]: 'Average number of darts', df_avg2.columns[1]: 'Std. Deviation'}
df_avg2 = df_avg2.rename(columns=mapping)

df_avg3 = df_avg2.sort_values('Average number of darts')
# df_avg3['Average number of darts'].round(decimals=1)

# Best checkout percentage
max_pc  = df_games['game_checkout_pc'].max()
# No. of darts for best checkout percentage
max_pc_num_darts =  df_games['total_darts'].min()

print("x")
# ------------ STREAMLIT CODE --------------------
st.title("Doubles Practice")

st.image('double8.jpg')
st.subheader(f"Practice sessions to date: {df_games.shape[0]}")
st.subheader(f"Best visit")
st.write(f"\tTotal darts to finish: {max_pc_num_darts}")
st.write(f"\tCheckout percentage: {max_pc}%")
st.subheader("Top 5 doubles")
st.write(df_avg3.head(5))
st.subheader("Bottom 5 doubles")
st.write(df_avg3.tail(5))


