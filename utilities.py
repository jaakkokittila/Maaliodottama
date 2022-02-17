import pandas as pd

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
