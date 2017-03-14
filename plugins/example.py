# -*- coding: utf-8 -*-

import longpoll


class Plugin(object):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("example", self.call)

    def call(self, event):
        if event.type == longpoll.VkEventType.MESSAGE_NEW:
            if event.text == '/ping':
                self.bot.api.messages.send(message="Pong!", peer_id=event.peer_id)
