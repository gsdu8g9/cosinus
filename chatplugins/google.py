from bot import AbstractChatPlugin

import urllib.parse

import requests
import lxml.html


class ChatPlugin(AbstractChatPlugin):
    help = """/google [запрос] - выдаёт ссылку на запрос в гугле, а также на первый результат"""

    def call(self, event):
        if event[0] != 4:
            return
        (q,__,p) = event[6].splitlines()[0].partition(' ')
    #   ^^^^^^^^ - парень с вытекающими глазами
        if q == '/google' and p:
            p_encoded = urllib.parse.quote_plus(p)
            search_url = 'https://www.google.com/search?q=' + p_encoded
            
            reply = []
            reply.append(search_url)

            try:
                rhead = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'}
                req = requests.get(search_url,headers=rhead)
                rtree = lxml.html.fromstring(req.text)
                lucky = rtree.xpath('//*/h3[@class="r"]/a')[0]
                reply.append(lucky.text_content())
                reply.append(lucky.get("href"))
            except:
                pass

            self.bot.vkapi.messages.send(message="\n".join(reply), peer_id=event[3])
