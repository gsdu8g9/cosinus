import random

import vk

from bot import vkapi

event_id = 4


def call(event):
  if event[0] == event_id:
    if event[6].partition(' ')[0] == '/Isin':
        r = '''Эта команда не доступна сейчас, и не думаю, что будет доступна когда-либо. 
Более того, её вообще не должно было быть, на самом деле.
Фотографий у меня тем более нет. Нигде, совсем, даже в Нидерландах.'''
        try:
            vkapi.messages.send(message=r, peer_id=event[3], random_id=random.randint(1, 12345678))
        except vk.exceptions.VkAPIError as e:
            if e.code != 9:
                raise
