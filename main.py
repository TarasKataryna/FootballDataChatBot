import application_settings as app_set
from telegran_bot import TelegramBot

if __name__ == '__main__':
        football_data_settings = {
            'competitions_url':app_set.COMPETITIONS_URL,
            'api_token': app_set.API_KEY,
            'team_url':app_set.TEAM_URL,
            'matches_url':app_set.COMPETITIONS_MATCHES_URL}
        TelegramBot(app_set.TELEGRAM_BOT_TOKEN, app_set.LUIS_API, football_data_settings).listen()