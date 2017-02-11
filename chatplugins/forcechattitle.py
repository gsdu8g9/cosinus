from bot import AbstractChatPlugin


class ChatPlugin(AbstractChatPlugin):
    def call(self, event):
        if event[0] != 4:
            return
        if (event[3] - 2000000000) not in self.bot.config['chat_titles'].keys():
            return
        if 'source_act' not in event[7]:
            return
        if event[7]['source_act'] != 'chat_title_update':
            return
        if int(event[7]['from']) == self.bot.bot_id:
            return
        print(event)
        self.bot.vkapi.messages.editChat(chat_id=event[3] - 2000000000,
                                         title=self.bot.config['chat_titles'][event[3] - 2000000000])
