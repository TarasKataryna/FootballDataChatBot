from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from luis_agent import Agent
from football_data import FootballData

class TelegramBot:
    def __init__(self, telegram_bot_key, luis_api, api_params):
        self.updater = Updater(token=telegram_bot_key)
        self.dispatcher = self.updater.dispatcher
        self.agent = Agent(luis_api)
        self.data_api_wrapper = FootballData(api_params['api_token'], api_params['competitions_url'],api_params['team_url'])
        pass

    def listen(self):
        self.add_handlers()
        self.updater.start_polling()
        pass

    def message_handler(self, bot, update):
        response_json = self.data_api_wrapper.get_competition_winner_in_season('PL', update.effective_message.text)
        handled_response = self.handle_response(response_json)
        bot.sendMessage(chat_id=update.message.chat_id, text=handled_response) 

    def add_handlers(self):
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_handler))

    def handle_response(self, response):
        if hasattr(response, 'message'):
            return response.message
        else:
            return response['team_name'] + '(id = {})'.format(response['team_id'])
    