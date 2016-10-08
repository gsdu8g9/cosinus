import vk

from bot import AbstractChatPlugin

event_id = 4


class ChatPlugin(AbstractChatPlugin):
    def call(self, event):
        if event[0] != event_id:
            return
        if event[6] == '/ping':
            self.bot.vkapi.messages.send(message="Pong!", peer_id=event[3])
        if event[6] == '/raise':
            self.bot.vkapi.messages.send(message="Raising exception", peer_id=event[3])
            raise Exception("Raised by /raise")
