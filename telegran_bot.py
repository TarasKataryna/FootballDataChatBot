from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

class TelegramBot:
    def __init__(self, telegram_bot_key):
        self.updater = Updater(token=telegram_bot_key)
        self.dispatcher = self.updater.dispatcher
        pass

    def listen(self):
        self.add_handlers()
        self.updater.start_polling()
        pass

    def message_handler(self, bot, update):
        print(update.effective_message.text)
        pass

    def add_handlers(self):
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.message_handler))