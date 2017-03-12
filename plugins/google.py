import urllib.parse

import requests
import lxml.html

import longpoll


class Plugin:
    help = """/google [запрос] - выдаёт ссылку на запрос в гугле, а также на первый результат"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("google", self.call)

    def call(self, event):
        if event.type != longpoll.VkEventType.MESSAGE_NEW:
            return
        if not event.text:
            return
        (q, __, p) = event.text.splitlines()[0].partition(' ')
        if q == '/google' and p:
            p_encoded = urllib.parse.quote_plus(p)
            search_url = 'https://www.google.ru/search?q=' + p_encoded

            reply = []
            reply.append(search_url)

            try:
                rhead = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
                req = requests.get(search_url, headers=rhead)
                rtree = lxml.html.fromstring(req.text)
                lucky = rtree.xpath('//*/h3[@class="r"]/a')[0]
                reply.append(lucky.text_content())
                reply.append(lucky.get("href"))
            except:
                pass

            self.bot.api.messages.send(message="\n".join(reply), peer_id=event.peer_id)
