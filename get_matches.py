import requests
import match_data as match_data
import sys

url='https://liiga.fi/api/v1/games?tournament=runkosarja&season='

#Season argument should be first in command line
season = sys.argv[1]
request = requests.get(url + season)

match_ids = []

matches = request.json()

for match in matches:
    if match['ended'] == True:
        match_ids.append(match['id'])

match_data.write_matches(match_ids, season)


