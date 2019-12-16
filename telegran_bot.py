from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from luis_agent import Agent
from football_data import FootballData

class TelegramBot:
    def __init__(self, telegram_bot_key, luis_api, api_params):
        self.updater = Updater(token=telegram_bot_key)
        self.dispatcher = self.updater.dispatcher
        self.agent = Agent(luis_api)
        self.data_api_wrapper = FootballData(api_params['api_token'], api_params['competitions_url'],api_params['team_url'], api_params['matches_url'])
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
        
    def handle_response(self, response):
        if hasattr(response, 'message'):
            return response.message
        else:
            return response['team_name'] + '(id = {})'.format(response['team_id'])


    def get_user_info(self, user_id):
         #USER HERE PROLOG DB TO GET USER BEST (DEFAULT) COMPETITION AND BEST (DEFAULT) TEAM
         return {'user_name': 'Taras', 'user_id':user_id, 'best_comp_id': '2021', 'best_comp_name': 'England'} 

    def handle_season_info_intent(self, user_info):
        if hasattr(user_info, 'best_comp_id'):
            return self.data_api_wrapper.get_matches(user_info['best_comp_id'])
        else:
            #ask user about his best competition
            pass