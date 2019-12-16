from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from luis_agent import Agent
from football_data import FootballData
from context import PrologKb

class TelegramBot:
    def __init__(self, telegram_bot_key, luis_api, api_params):
        self.updater = Updater(token=telegram_bot_key)
        self.dispatcher = self.updater.dispatcher
        self.agent = Agent(luis_api)
        self.data_api_wrapper = FootballData(api_params['api_token'], api_params['competitions_url'],api_params['team_url'], api_params['matches_url'])
        self.prolog = PrologKb()
        pass

    def listen(self):
        self.add_handlers()
        self.updater.start_polling()
        pass

    def message_handler(self, bot, update):
        user_info = self.get_user_info(update.effective_user.id)
        handled_response = self.handle_user_message(update.effective_message.text, user_info)
        bot.sendMessage(chat_id=update.message.chat_id, text=handled_response) 

    def add_handlers(self):
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_handler))

    def handle_user_message(self, message, user_info):
        luis_response = self.agent.send_message(message)
        intent = luis_response.intents[0].intent

        if intent == 'Greeting':
            return {'message': "Hello!"}
        elif intent == 'SeasonInfo':
            res_json = self.handle_season_info_intent(user_info)
            return self.handle_response(res_json)
        elif intent == 'MatchesInfo':
            res_json = self.handle_matches_info_intent(user_info)
            return self.handle_response(res_json)
        elif intent == 'GetCompetition':
            res_json = self.handle_get_competition_intent(user_info, luis_response)
            return self.handle_response(res_json)

        
    def handle_response(self, response):
        if 'message' in response:
            return response.message
        elif 'team_name' in response:
            return response['team_name'] + '(id = {})'.format(response['team_id'])
        elif 'matches' in response:
            return_string = ''
            for i in response['matches']:
                return_string = return_string + i['home_team_name'] + ' ({}) '.format(i['home_team_id']) + str(i['home_team_score']) + ' - ' + str(i['away_team_score']) + ' ' + i['away_team_name'] + ' ({})\n'.format(i['away_team_id'])
            return return_string

    def get_user_info(self, user_id):
        try:
            comp_id = self.prolog.get_user_competitions(user_id)[0]
            return {'user_id':user_id, 'best_comp_id': str(comp_id)} 
        except Exception as ex:
            return {'user_id':user_id}
            

    def handle_season_info_intent(self, user_info):
        if 'best_comp_id' in user_info:
            return self.data_api_wrapper.get_competition_winner_in_season('2021', 2018)
        else:
            return {'message': 'Please, provide competition id.'}

    
    def handle_matches_info_intent(self, user_info):
        if 'best_comp_id' in user_info:
            return self.data_api_wrapper.get_matches(user_info['best_comp_id'])
        else:
            return {'message': 'Please, provide competition id.'}

    def handle_get_competition_intent(self, user_info, intent_data):
        comp_id = intent_data.entities[0].entity
        if 'best_comp_id' not in user_info:
            self.prolog.add_user_competition(user_info['user_id'], comp_id)
            return {'message':'We just set this competition id as default'}
            