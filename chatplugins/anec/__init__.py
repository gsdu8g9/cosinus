import random

from bot import AbstractChatPlugin

from .anecs import anecs


class ChatPlugin(AbstractChatPlugin):
    help = '''/анекдот - рассказать очень смешной анекдот'''

    def call(self, event):
        if event[0] != 4:
            return
        if event[6].partition(' ')[0] == '/анекдот':
            try:
                n = int(event[6].partition(' ')[2])
                if not (0 < n < len(anecs)):
                    raise ValueError()
            except ValueError:
                n = random.randint(1, len(anecs) + 1)
            self.bot.vkapi.messages.send(message='Анекдот %d\n%s' % (n, anecs[n - 1]), peer_id=event[3])
