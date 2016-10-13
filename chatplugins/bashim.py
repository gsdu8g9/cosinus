import requests
import lxml.html
from bot import AbstractChatPlugin


class ChatPlugin(AbstractChatPlugin):
    help = '''/bash - рассказать очень смешной анекдот'''
    def __init__(self, bot):
        super(ChatPlugin,self).__init__(bot)
        self.randomcache = []

    def call(self, event):
        if event[0] == 4 and event[6].partition(' ')[0] == '/bash':
            try:
                try:
                    int(event[6].partition(' ')[2]) # Должно заорать
                    req = requests.get('http://bash.im/quote/%s' % event[6].partition(' ')[2], allow_redirects=False)
                    if req.status_code == 302:
                        raise ValueError
                    req.raise_for_status()
                    rtree = lxml.html.fromstring(req.text)
                    quote = rtree.xpath('//*/div[@class="quote"]')[0]
                    q_id = quote.xpath('*/a[@class="id"]/text()')[0]
                    q_text = '\n'.join(quote.xpath('div[@class="text"]/text()'))
                except ValueError:
                    if not self.randomcache:
                        req = requests.get('http://bash.im/random')
                        req.raise_for_status()
                        rtree = lxml.html.fromstring(req.text)
                        quotes = rtree.xpath('//*/div[@class="quote"]')
                        for quote in quotes:
                            try:
                                rq_id = quote.xpath('*/a[@class="id"]/text()')[0]
                                rq_text = '\n'.join(quote.xpath('div[@class="text"]/text()'))
                                self.randomcache.append((rq_id, rq_text))
                            except:
                                pass
                    (q_id, q_text) = self.randomcache.pop()
                response = ("Цитата {id}\n{text}").format(id=q_id,text=q_text)
            except requests.exceptions.ConnectionError:
                response = "Не удалось подключиться к серверу bash.im"


            
            
            self.bot.vkapi.messages.send(message=response, peer_id=event[3])
