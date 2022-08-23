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


def sort_MLB_standings(standings):
    MLBTeamList = []
    for i in [200, 201, 202, 203, 204, 205]:
        for j in range(5):
            wins = standings[i]['teams'][j]['w']
            losses = standings[i]['teams'][j]['l']
            win_frac = wins / (wins + losses)
            mlbTeam = {
                'name': standings[i]['teams'][j]['name'],
                'wins': wins,
                'losses': losses,
                'win_frac': round(win_frac, 4)
            }
            MLBTeamList.append(mlbTeam)
    sortedMLBTeams = sorted(MLBTeamList, key = lambda i: i['name'])
    return sortedMLBTeams


class FantTeam:
    def __init__(self, name):
        self.name = name
        self.teams = []

    def get_name(self):
        return self.name
    
    def get_teams(self):
        return self.teams

    def add_team(self, mlbTeamData):
        self.teams.append(mlbTeamData)

    def sort_teams(self):
        self.teams = sorted(self.teams, key = lambda i: i['win_frac'], reverse=True)
    
    def get_totals(self):
        return {
            'name': self.name,
            'wins': self.teams[4]['wins'],
            'losses': self.teams[4]['losses'],
            'win_frac': self.teams[4]['win_frac']
        }

class FantTeamEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def discrete_fant_data(sortedMLBTeams):
    names = ["Team Collins", "Team Donofrio", "Team Ludwig", "Team Luvin", "Team McGowan", "Team Schmidt", "Team Shannon"]
    collins = [5, 6, 13, 21]
    donofrio = [9, 12, 20, 26]
    ludwig = [1, 7, 23, 27]
    luvin = [11, 15, 17, 18]
    mcgowan = [2, 3, 16, 22]
    schmidt = [0, 4, 8, 29]
    shannon = [10, 19, 25, 28]
    teams_i = [collins, donofrio, ludwig, luvin, mcgowan, schmidt, shannon]

    teams_names = []
    for i in range(7):
        teams_names.append({
            'name': names[i],
            'teams': teams_i[i]
        })

    fant_data = []
    for i in range(len(teams_names)):
        wins = 0
        losses = 0
        win_frac = 0
        team_info = FantTeam(teams_names[i]['name'])
        for team_i in teams_names[i]['teams']:
            team_info.add_team(sortedMLBTeams[team_i])
            wins += sortedMLBTeams[team_i]['wins']
            losses += sortedMLBTeams[team_i]['losses']

        win_frac = wins / (wins + losses)
        team_info.sort_teams()
        team_info.add_team({
            'name': 'TOTAL',
            'wins': wins,
            'losses': losses,
            'win_frac': round(win_frac, 4)
        })
        fant_data.append(team_info)

    return fant_data


def calc_fant_standings(fant_data):
    totals = []
    for team in fant_data:
        totals.append(team.get_totals())

    sorted_fant_stand = sorted(totals, key = lambda i: i['win_frac'], reverse = True)
    return sorted_fant_stand


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
    sorted_stand = sort_MLB_standings(curr_stand)
    fant_info = discrete_fant_data(sorted_stand)
    fant_standings = calc_fant_standings(fant_info)
    
    return {
        'statusCode': 200,
        'body': json.dumps(fant_standings),
        'headers': {
            'Access-Control-Allow-Origin': '*'
        }
    }

# print(lambda_handler({},{}))
