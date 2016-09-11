import random
import re

from bot import vkapi, bot_id

event_id = 4

emotes = vkapi.photos.get(album_id=228083099)['items']


def call(event):
  if event[0] == event_id:
    a = []
    for emote in emotes:
        if re.compile(r'\b({0})\b'.format(emote['text'])).search(event[6]) is not None:
            a += ['photo' + str(bot_id) + '_' + str(emote['id'])]
    a = ','.join(a)
    if a != '':
        vkapi.messages.send(message=str(random.random()), attachment=a, peer_id=event[3])
