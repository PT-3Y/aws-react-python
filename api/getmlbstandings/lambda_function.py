import statsapi
from datetime import date
import json
from json import JSONEncoder

#gets today's MLB standings
# updated after the season ended to just include final 2020 standings
def get_MLB_standings():
    #get today's date so we can get the updated standings
    today = date.today()
    month = today.month
    day = today.day
    year = today.year
    print(year)
    if year > 2020 or (year == 2020 and month > 10):
        season = 2020
        d_m_y = None
    else:
        season = None
        d_m_y = str(month) + "/" + str(day) + "/" + str(year)
        
    standings = statsapi.standings_data(division="all", include_wildcard=True, season=season, standingsTypes=None, date=d_m_y)
    return standings

def parse_MLB_standings(standings):
    standings_list = []
    for i in [200, 201, 202, 203, 204, 205]:
        standings_list.append(standings[i])
    return standings_list

def lambda_handler(event, context):
    curr_stand = get_MLB_standings()
    if not curr_stand:
        return {
            'statusCode': 500,
            'body': "Call to MLB-StatsAPI failed",
            'headers': {
            'Access-Control-Allow-Origin': '*'
            }
        }
    stand_list = parse_MLB_standings(curr_stand)

    return {
        'statusCode': 200,
        'body': json.dumps(stand_list),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }
