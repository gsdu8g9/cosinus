import random
import re

import longpoll


class Plugin:
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("kappa", self.call)
        self.emotes = self.bot.api.photos.get(album_id=self.bot.config["kappa"])['items']

    def call(self, event):
        if event.type != longpoll.VkEventType.MESSAGE_NEW:
            return
        a = list()
        for emote in self.emotes:
            if re.compile(r'\b({0})\b'.format(emote['text'])).search(event.text) is not None:
                a += ['photo%d_%d' % (self.bot.bot_id, emote['id'])]
        a = ','.join(a)
        if a != '':
            self.bot.api.messages.send(random_id=random.randint(1, 12345678), attachment=a, peer_id=event.peer_id)
