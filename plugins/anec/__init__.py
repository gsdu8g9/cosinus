import json
import os
import random

from bot import vkapi

anec = json.load(open(os.path.join(os.path.dirname(__file__), 'anec.json'), encoding='utf8'))

event_id = 4


def call(event):
    if event[6].partition(' ')[0] == '/анекдот':
        vkapi.messages.send(message=random.choice(anec), peer_id=event[3])
