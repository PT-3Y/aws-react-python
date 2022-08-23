import statsapi
from datetime import date
import requests
import json
from flask import Flask, make_response, jsonify
from json import JSONEncoder

app = Flask(__name__)

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

    #returns the standings sorted by division.
    #200 = AL West, 201 = AL East, 202 = AL Central, 203 = NL West, 204 = NL East, 205 = NL Central
    standings = statsapi.standings_data(division="all", include_wildcard=True, season=season, standingsTypes=None, date=d_m_y)
    print(standings)
    return standings

# convert to a list, get rid of the division #s. Each object in the list contains:
# { 
#     'div_name': <div_name>
#     'teams': [array of teams w/ their info]
# }
def parse_MLB_standings(standings):
    standings_list = []
    for i in [200, 201, 202, 203, 204, 205]:
        standings_list.append(standings[i])
    return standings_list


#standings_ = statsapi.standings(date='08/07/2020', include_wildcard=False)
#print( standings_ )

# First, i'm going to sort the data by Fantasy team
# So i'll discard the elimination numbers and team IDs
# extract the desired data: team name

# sorts the standings alphabetically by team location and discards the irrelevant data
def sort_MLB_standings(standings):
    # first i'm going to put all the MLB team objects (name, wins, losses) into a list
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
    #sort alphabetically by location name
    sortedMLBTeams = sorted(MLBTeamList, key = lambda i: i['name'])
    return sortedMLBTeams


#create a class that has each MLB team data. Will make it easier
#to then put in 
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

# returns a list of FantTeam objects, one for each person's team
def discrete_fant_data(sortedMLBTeams):
    #indices of sorted teams for each person
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
    # print(teams_names)

    #a list of FantTeam objects, which have the person's name as a field, and their team data 
    # a list with team objects, containing the team name, wins, and losses (sorted by win_frac),
    # as well as the TOTAL wins, losses, and win_frac.
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
        # add the total to the end
        team_info.add_team({
            'name': 'TOTAL',
            'wins': wins,
            'losses': losses,
            'win_frac': round(win_frac, 4)
        })
        fant_data.append(team_info)

    return fant_data

#calculate the current fantasy standings, returns
# a list with each person's name, wins, loss, and win_frac
def calc_fant_standings(fant_data):
    totals = []
    for team in fant_data:
        totals.append(team.get_totals())

    # get the standings by sorting by win_frac
    sorted_fant_stand = sorted(totals, key = lambda i: i['win_frac'], reverse = True)
    return sorted_fant_stand


# now, i need to send the data over to React. I may actually need to use MongoDB to store this data?
# this way, I can have this python script run at like 2AM, get the new data from the mlbstats API,
# calculate the standings, and then update the DB so that React only needs to request the static
# data from the DB rather than recalculate every time? idk. 

#i'll send it using Flask

@app.route('/getfantasystandings', methods = ['GET'])
def send_updated_standings():

    curr_stand = get_MLB_standings()
    if not curr_stand:
        resp = make_response("Call to MLB-StatsAPI failed", 500)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    sorted_stand = sort_MLB_standings(curr_stand)
    fant_info = discrete_fant_data(sorted_stand)
    fant_standings = calc_fant_standings(fant_info)

    #print(json.dumps(fant_standings))

    resp = make_response(json.dumps(fant_standings), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
 
    return resp

@app.route('/getteaminfo', methods = ['GET'])
def send_team_info():
    curr_stand = get_MLB_standings()
    if not curr_stand:
        resp = make_response("Call to MLB-StatsAPI failed", 500)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    sorted_stand = sort_MLB_standings(curr_stand)
    fant_info = discrete_fant_data(sorted_stand)

    # print(json.dumps(fant_info, cls=FantTeamEncoder))

    resp = make_response(json.dumps(fant_info, cls=FantTeamEncoder), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
 
    return resp

@app.route('/getmlbstandings', methods = ['GET'])
def send_mlb_standings():
    curr_stand = get_MLB_standings()
    if not curr_stand:
        resp = make_response("Call to MLB-StatsAPI failed", 500)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    stand_list = parse_MLB_standings(curr_stand)
    resp = make_response(json.dumps(stand_list))
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

if __name__ == '__main__':
    app.run(host='localhost', port=3001)