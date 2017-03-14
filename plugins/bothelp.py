import longpoll


class Plugin:
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("bothelp", self.call)

    def call(self, event):
        if (event.type == longpoll.VkEventType.MESSAGE_NEW
                and event.text.partition(' ')[0] == '/help'
                and event.peer_id < longpoll.CHAT_START_ID):
            respond = []
            respond += ['Помощь:']
            for plugin in self.bot.plugins.values():
                if hasattr(plugin, 'help'):
                    respond.append(str(plugin.help))
            respond += ['Подробнее: https://hdk5.xyz/cosine']

            self.bot.api.messages.send(message='\n'.join(respond), peer_id=event.peer_id)
