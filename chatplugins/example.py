import vk

from bot import AbstractChatPlugin

event_id = 4


class ChatPlugin(AbstractChatPlugin):
    def call(self, event):
        if event[0] != event_id:
            return
        if event[6] == '/ping':
            try:
                self.bot.vkapi.messages.send(message="Pong!", peer_id=event[3])
            except vk.exceptions.VkAPIError as e:
                if e.code != 9:
                    raise
