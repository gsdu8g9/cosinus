# -*- coding: utf-8 -*-

import random

import longpoll
from .anecs import anecs


class Plugin:
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("anecs", self.call)

    help = '''/анекдот - рассказать очень смешной анекдот'''

    def call(self, event):
        if event.type != longpoll.VkEventType.MESSAGE_NEW:
            return
        if event.text.partition(' ')[0] == '/анекдот':
            try:
                n = int(event.text.partition(' ')[2])
                if not (0 < n <= len(anecs)):
                    raise ValueError()
            except ValueError:
                n = random.randint(1, len(anecs) + 1)
            self.bot.api.messages.send(message='Анекдот %d\n%s' % (n, anecs[n - 1]), peer_id=event.peer_id)
