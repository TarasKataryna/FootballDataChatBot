import requests

class FootballData:
    def __init__(self, api_token, competition_api_url, team_api_url) :
        self.competition_api_url = competition_api_url
        self.team_api_url = team_api_url
        self.api_token = api_token


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

