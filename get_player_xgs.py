import pandas as pd
import utilities as utils
import csv

shots = pd.read_csv('data/shots_for_prediction.csv')
players = pd.read_csv('data/players.csv', encoding='cp1252')
shots_2022 = shots.iloc[147062:len(shots)]

def normalize_player_spelling(name):
    names = name.split(' ')
    names[0] = names[0][0] + names[0][1:len(names[0])].lower()
    names[1] = names[1][0] + names[1][1:len(names[1])].lower()

    return names[0] + ' ' + names[1]

def get_player_name(player_id):
    players = pd.read_csv('data/players.csv', encoding='cp1252')
    player = players[players['Id'] == player_id]

    player_name = player['Name'].iloc[0]

    return player_name

player_xgs = []

for i, player in players.iterrows():
    player_id = player['Id']
    player_shots = shots_2022[shots_2022['Shooter'] == int(player_id)]

    if len(player_shots) > 10:
        player_shots_for_prediction = player_shots[['Shot_x', 'Shot_y', 'Previous_shots', 'On_empty_net', 'Type_EvenStrengthShot', 'Type_PowerplayShot', 'Type_ShorthandedShot']]

        player_xg = utils.get_xg(player_shots_for_prediction)
        player_name = normalize_player_spelling(get_player_name(player_id))

        player_xgs.append({'Player': player_name, 'XG': player_xg})

field_names = ['Pelaaja', 'XG']
sorted_xgs = sorted(player_xgs, reverse=True, key=lambda x: x['XG'])

with open('data/player_xgs.csv', mode='w', encoding='cp1252') as player_xg_file:
    player_writer = csv.DictWriter(player_xg_file, fieldnames=field_names)
    player_writer.writeheader()

    for player in sorted_xgs:
        player_writer.writerow({'Pelaaja': player['Player'], 'XG': player['XG']})

    player_xg_file.close()
