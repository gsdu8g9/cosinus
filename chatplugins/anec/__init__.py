import json
import os
import random

from bot import AbstractChatPlugin

anec = json.load(open(os.path.join(os.path.dirname(__file__), 'anec.json'), encoding='utf8'))

event_id = 4

class ChatPlugin(AbstractChatPlugin):
    def call(self, event):
      if event[0] == event_id:
        if event[3] < 2000000000 and event[6].partition(' ')[0] == '/анекдот':
            try:
                n = int(event[6].partition(' ')[2])
            except ValueError:
                n = random.randint(0, len(anec) - 1)
            self.bot.vkapi.messages.send(message='Анекдот ' + str(n) + '\n' + anec[n], peer_id=event[3])
