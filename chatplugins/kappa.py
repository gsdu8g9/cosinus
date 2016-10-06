import random
import re

from bot import AbstractChatPlugin

event_id = 4


class ChatPlugin(AbstractChatPlugin):
    def __init__(self, bot):
        super(ChatPlugin, self).__init__(bot)
        self.emotes = self.bot.vkapi.photos.get(album_id=228083099)['items']


    def call(self, event):
        if event[0] != event_id:
            return
        a = []
        for emote in self.emotes:
            if re.compile(r'\b({0})\b'.format(emote['text'])).search(event[6]) is not None:
                a += ['photo' + str(self.bot.bot_id) + '_' + str(emote['id'])]
        a = ','.join(a)
        if a != '':
            self.bot.vkapi.messages.send(message=str(random.random()), attachment=a, peer_id=event[3])
