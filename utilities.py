import pandas as pd
import pickle
import requests

# These are functions that are used in multiple files

def read_dataframe(path, encoding):
    try:
        return pd.read_csv(path, encoding=encoding)
    except:
        return None

def check_if_row_in_dataframe(row_id, df):
    if df is None:
        return False
    else:
        return len(df[df['Id'] == int(row_id)]) > 0

def get_xg(shots):
    model = pickle.load(open('knn_model', 'rb'))

    predictions = model.predict(shots)
    xg = sum(predictions)

    return xg

def get_match_ids(season):
    url = url='https://liiga.fi/api/v1/games?tournament=runkosarja&season=' + season
    request = requests.get(url)

    matches = request.json()
    match_ids = []

    for match in matches:
        if match['ended'] == True:
            match_ids.append(match['id'])

    return match_ids

