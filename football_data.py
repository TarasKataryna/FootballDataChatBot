import requests
from datetime import date, timedelta

class FootballData:
    def __init__(self, api_token, competition_api_url, team_api_url, matches_api_url) :
        self.competition_api_url = competition_api_url
        self.team_api_url = team_api_url
        self.api_token = api_token
        self.matches_api_url = matches_api_url


    def add_request_headers(self):
        return {'X-Auth-Token': self.api_token}

    def get_competitions(self, comp_id):
        headers = self.add_request_headers()
        r = requests.get(self.competition_api_url + comp_id, headers=headers)
        return r.json()

    def get_competition_winner_in_season(self, com_id, season):
        result = self.get_competitions(com_id)
        seasonResult = list(filter(lambda x: x['startDate'].split('-')[0] == str(season), result['seasons']))[0]
        result = {}
        try:
            result['team_name'] = seasonResult['winner']['name']
            result['team_id'] = seasonResult['winner']['name']
        except Exception as ex:
            result['message'] = "Sorry, but there aren\'t information about winner of this season"
         
        return result

    def get_matches(self, comp_id):
        params = {'dateTo': date.today(),'dateFrom':date.today() - timedelta(days=10)}
        headers = self.add_request_headers()
        r = requests.get(self.matches_api_url.format(comp_id), headers=headers, params=params).json()
        result = {'matches':[]}
        try:
            for match in r['matches']:
                result['matches'].append({
                    'away_team_name':match['awayTeam']['name'],
                    'away_team_id':match['awayTeam']['id'],
                    'away_team_score':match['score']['fullTime']['awayTeam'],
                    'home_team_name':match['homeTeam']['name'],
                    'home_team_id':match['homeTeam']['id'],
                    'home_team_score':match['score']['fullTime']['homeTeam']
                    })
            return result
        except:
            return result


        
