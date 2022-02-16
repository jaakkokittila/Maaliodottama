import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsRegressor
import csv

shots = pd.read_csv('data/shots_for_prediction.csv')
matches = pd.read_csv('data/matches.csv', encoding='cp1252')

model = pickle.load(open('knn_model', 'rb'))

def get_team_xg(team, match_shots):
    team_shots = match_shots[match_shots['Shooting_team'] == team]
    team_predictor_features = team_shots[['Shot_x', 'Shot_y', 'Previous_shots', 'Type_EvenStrengthShot', 'Type_PowerplayShot', 'Type_ShorthandedShot']]

    team_predictions = model.predict(team_predictor_features)
    team_xg = sum(team_predictions)

    return team_xg

def get_match_xg(match_id):
    match_shots = shots[shots['Match_id'] == int(match_id)]

    match_teams = match_shots.Shooting_team.unique()

    home_xg = get_team_xg(match_teams[0], match_shots)
    away_xg = get_team_xg(match_teams[1], match_shots)

    return home_xg, away_xg

field_names = ['Match_id', 'Home_name', 'Home_goals', 'Home_xg', 'Away_name', 'Away_goals', 'Away_xg']

with open('data/match_expected_goals.csv', mode='w', encoding='cp1252') as xg_file:
    xg_writer = csv.DictWriter(xg_file, fieldnames=field_names)
    xg_writer.writeheader()

    for i, match in matches.iterrows():
        match_id = match['Match_id']

        home_name = match['Home_name']
        away_name = match['Away_name']

        home_score = match['Home_score']
        away_score = match['Away_score']

        home_xg, away_xg = get_match_xg(match_id)

        xg_writer.writerow({'Match_id': match_id, 'Home_name': home_name, 'Home_goals': home_score, 'Home_xg': home_xg,
                            'Away_name': away_name, 'Away_goals': away_score, 'Away_xg': away_xg})

    xg_file.close()