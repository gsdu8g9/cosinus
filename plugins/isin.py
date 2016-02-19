import random
import re

import vk

from bot import vkapi

event_id = 4


def call(event):
    if event[3] != 2000000001 and ( event[6].partition(' ')[0] == '/Isin' or re.compile(
            r'\b(Женя|Жени|Жене|Женю|Женей|Жень|Евгений Сергеевич)\b').search(event[6]) is not None):
        isin = vkapi.photos.get(album_id=227998943)
        rid = random.choice(isin['items'])['id']
        r = "Isin_photo=" + str(rid)
        a = 'photo348580470_' + str(rid)
        try:
            vkapi.messages.send(message=r, attachment=a, peer_id=event[3])
        except vk.exceptions.VkAPIError as e:
            if e.code != 9:
                raise
