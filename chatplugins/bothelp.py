import vk

from bot import AbstractChatPlugin


class ChatPlugin(AbstractChatPlugin):
    def call(self, event):
      if event[0] == 4:
        if event[6].partition(' ')[0] == '/help' and event[3] < 2000000000:
            respond = []
            respond += ['Инструкция по применению:']
            for name, plugin in self.bot.chatplugins.items():
                if hasattr(plugin, 'help'):
                    respond.append(str(plugin.help))
            respond += ['Подробнее: https://hdk5.xyz/cosine']

            self.bot.vkapi.messages.send(message='\n'.join(respond), peer_id=event[3])
