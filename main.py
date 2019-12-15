import application_settings as app_set
from telegran_bot import TelegramBot

if __name__ == '__main__':
        TelegramBot(app_set.TELEGRAM_BOT_TOKEN).listen()