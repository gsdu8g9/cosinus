import vk
from bot import vkapi

event_id = 4


def call(event):
    if event[6] == '/ping':
        try:
            vkapi.messages.send(message="Pong!", peer_id=event[3])
        except vk.exceptions.VkAPIError as e:
            if e.code != 9:
                raise
