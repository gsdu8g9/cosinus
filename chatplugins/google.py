from bot import AbstractChatPlugin

event_id = 4


class ChatPlugin(AbstractChatPlugin):
    def call(self, event):
        if event[0] != event_id:
            return
        if event[6].partition(' ')[0] == '/google':
            search_request = event[6].partition(' ')[2].partition('\n')[0]
            search_request = search_request.replace('+', '%2B')
            search_request = search_request.replace('&', '%26')
            search_request = search_request.replace(' ', '+')
            search_url = 'https://www.google.com/search?q=' + search_request
            self.bot.vkapi.messages.send(message=search_url, peer_id=event[3])
