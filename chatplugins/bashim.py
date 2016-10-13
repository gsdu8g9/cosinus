import requests
import lxml.html
from bot import AbstractChatPlugin


class ChatPlugin(AbstractChatPlugin):
    help = '''/bash - рассказать очень смешной анекдот'''
    def call(self, event):
        if event[0] == 4 and event[6].partition(' ')[0] == '/bash':
            try:
                int(event[6].partition(' ')[2]) # Должно заорать
                req = requests.get('http://bash.im/quote/%s' % event[6].partition(' ')[2], allow_redirects=False)
                if req.status_code == 302:
                    raise ValueError
            except ValueError:
                req = requests.get('http://bash.im/random')
            req.raise_for_status()
            rtree = lxml.html.fromstring(req.text)
            quote = rtree.xpath('//*/div[@class="quote"]')[0]
            q_id = quote.xpath('*/a[@class="id"]/text()')[0]
            q_text = '\n'.join(quote.xpath('div[@class="text"]/text()'))
            response = ("Цитата {id}\n{text}").format(id=q_id,text=q_text)
            self.bot.vkapi.messages.send(message=response, peer_id=event[3])
