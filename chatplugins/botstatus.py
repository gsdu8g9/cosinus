import datetime

import vk

from bot import AbstractChatPlugin

event_id = 4


class ChatPlugin(AbstractChatPlugin):
    def __init__(self,bot):
        super(ChatPlugin, self).__init__(bot)
        self.start_time = datetime.datetime.now()

    def call(self, event):
        if event[0] != event_id:
            return
        if event[6].partition(' ')[0] == '/status' and event[3] < 2000000000:
            try:
                self.bot.vkapi.messages.send(message='Я жив ' + str(datetime.datetime.now() - self.start_time), peer_id=event[3])
            except vk.exceptions.VkAPIError as e:
                if e.code != 9:
                    raise

       