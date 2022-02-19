import pandas as pd
import csv
import utilities as utils

shots = pd.read_csv('data/shots_for_prediction.csv')
matches = pd.read_csv('data/matches.csv', encoding='cp1252')

def get_match_xg(match_id, home_id, away_id):
    match_shots = shots[shots['Id'] == int(match_id)]

    home_shots = match_shots[match_shots['Shooting_team'] == home_id]
    home_predictor_features = home_shots[['Shot_x', 'Shot_y', 'Previous_shots', 'On_empty_net', 'Type_EvenStrengthShot', 'Type_PowerplayShot', 'Type_ShorthandedShot']]

    away_shots = match_shots[match_shots['Shooting_team'] == away_id]
    away_predictor_features = away_shots[['Shot_x', 'Shot_y', 'Previous_shots', 'On_empty_net', 'Type_EvenStrengthShot', 'Type_PowerplayShot', 'Type_ShorthandedShot']]

    home_xg = utils.get_xg(home_predictor_features)
    away_xg = utils.get_xg(away_predictor_features)

    return home_xg, away_xg

field_names = ['Id', 'Home_name', 'Home_goals', 'Home_xg', 'Away_name', 'Away_goals', 'Away_xg']

with open('data/match_expected_goals.csv', mode='w', encoding='cp1252') as xg_file:
    xg_writer = csv.DictWriter(xg_file, fieldnames=field_names)
    xg_writer.writeheader()

    for i, match in matches.iterrows():
        match_id = match['Id']

        home_name = match['Home_name']
        away_name = match['Away_name']

        home_score = match['Home_score']
        away_score = match['Away_score']

        home_xg, away_xg = get_match_xg(match_id, match['Home_id'], match['Away_id'])

        xg_writer.writerow({'Id': match_id, 'Home_name': home_name, 'Home_goals': home_score, 'Home_xg': home_xg,
                            'Away_name': away_name, 'Away_goals': away_score, 'Away_xg': away_xg})

    xg_file.close()