import datetime

import vk

from bot import vkapi, start_time

event_id = 4


def call(event):
    if event[6].partition(' ')[0] == '/status' and event[3] < 2000000000:
        try:
            vkapi.messages.send(message='Я жив ' + str(datetime.datetime.now() - start_time), peer_id=event[3])
        except vk.exceptions.VkAPIError as e:
            if e.code != 9:
                raise
