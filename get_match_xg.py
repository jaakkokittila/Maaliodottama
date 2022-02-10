import pandas as pd
import sys
import pickle
from sklearn.neighbors import KNeighborsRegressor

shots = pd.read_csv('data/shots_for_prediction.csv')

# Match id should be first argument in command line
match = sys.argv[1]

team_names = {624554857: 'Lukko', 651304385: 'TPS', 951626834: 'Ilves', 219244634: 'JYP',
              875886777: 'Pelicans', 933686567: 'SaiPa', 168761288: 'HIFK', 292293444: 'Jukurit',
              461765763: 'KooKoo', 859884935: 'KalPa', 495643563: 'Kärpät', 679171680: 'Ässät',
              55786244: 'HPK', 626537494: 'Sport', 362185137: 'Tappara'}

model = pickle.load(open('knn_model', 'rb'))

match_shots = shots[shots['Match_id'] == int(match)]

match_teams = match_shots.Shooting_team.unique()

for team in match_teams:
    team_name = team_names.get(team)

    team_shots = match_shots[match_shots['Shooting_team'] == team]
    team_predictor_features = team_shots[['Shot_x', 'Shot_y', 'Previous_shots', 'Type_EvenStrengthShot', 'Type_PowerplayShot', 'Type_ShorthandedShot']]

    team_predictions = model.predict(team_predictor_features)
    team_xg = sum(team_predictions)

    print(team_name, ': ', team_xg)
