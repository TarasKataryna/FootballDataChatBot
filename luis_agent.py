import luis

class Agent:
    def __init__(self, api_url):
        self.l = luis.Luis(api_url)

    def send_message(self, message):
        return self.l.analyze(message)
