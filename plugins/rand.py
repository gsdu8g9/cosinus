import random

class Plugin:
    event_id=4

    def __init__(self, vkapi):
        self.vkapi = vkapi

    def __call__(self, event):
        if event[6] == '/random':
            self.vkapi.messages.send(message=str(random.random()),peer_id=event[3])
            return True
        return False
