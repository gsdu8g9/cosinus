from bot import AbstractChatPlugin

import requests
import lxml.html

event_id = 4


class ChatPlugin(AbstractChatPlugin):
    help = """/google [запрос] - выдаёт ссылку на запрос в гугле, а также на первый результат"""

    def call(self, event):
        if event[0] != event_id:
            return
        if event[6].partition(' ')[0] == '/google':
            search_request = event[6].partition(' ')[2].partition('\n')[0]
            search_request = search_request.replace('+', '%2B')
            search_request = search_request.replace('&', '%26')
            search_request = search_request.replace(' ', '+')
            search_url = 'https://www.google.com/search?q=' + search_request

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
