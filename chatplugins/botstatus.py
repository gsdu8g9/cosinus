import datetime

from bot import AbstractChatPlugin
import _thread


class ChatPlugin(AbstractChatPlugin):
    help = """/status - узнать аптайм бота (ЛС)"""

    def __init__(self, bot):
        super(ChatPlugin, self).__init__(bot)
        self.start_time = datetime.datetime.now()

    def call(self, event):
        if event[0] != 4:
            return
        if event[6].partition(' ')[0] == '/status' and event[3] < 2000000000:
            self.bot.vkapi.messages.send(message='Я жив ' + str(datetime.datetime.now() - self.start_time), peer_id=event[3])
        elif event[6].partition(' ')[0] == '/kill' and event[3] in self.config["bot"]["admins"]:
            print("Killed by", event[3])
            self.bot.vkapi.messages.send(message='Умираю', peer_id=event[3])
            _thread.interrupt_main()
