import json
import os
import random

from bot import vkapi

anec = json.load(open(os.path.join(os.path.dirname(__file__), 'anec.json'), encoding='utf8'))

event_id = 4


def call(event):
    if event[6].partition(' ')[0] == '/анекдот':
        try:
            n = int(event[6].partition(' ')[2])
        except ValueError:
            n = random.randint(0,len(anec)-1)
        vkapi.messages.send(message='Анекдот '+ str(n) + '\n' + anec[n], peer_id=event[3])
