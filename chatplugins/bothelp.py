import vk

from bot import AbstractChatPlugin

event_id = 4


class ChatPlugin(AbstractChatPlugin):
    """Должен инициализироваться раньше остальных плагинов чата"""
    def __init__(self, bot):
        super(ChatPlugin, self).__init__(bot)
        self.bot.chat_help = []

    def call(self, event):
      if event[0] == event_id:
        if event[6].partition(' ')[0] == '/help' and event[3] < 2000000000:
            respond = []
            respond += ['Инструкция по применению:']

            respond += self.bot.chat_help  # Должно инициализироваться плагинами. Но пока так

            try:
                self.bot.vkapi.messages.send(message='\n'.join(respond), peer_id=event[3])
            except vk.exceptions.VkAPIError as e:
                if e.code != 9:
                    raise
