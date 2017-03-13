import io
import os
from random import randint

import requests

import longpoll


class Plugin:
    help = """/pony - присылает в ответ случайную картинку с поняшкой, /котик - c котиком"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("pone", self.call)
        self.update_ib_sid()

    def update_ib_sid(self):
        req = requests.get("https://inkbunny.net/api_login.php?"
                           "username={username}&password={password}".format(username=os.environ.get('INKBUNNY_LOGIN', 'guest'),
                                                                            password=os.environ.get('INKBUNNY_PASS', '')))
        resp = req.json()
        if 'error_code' in resp:
            raise Exception
        self.ib_sid = resp['sid']

    def get_ib(self, query):
        req = requests.get("https://inkbunny.net/api_search.php?sid={sid}&text={query}&"
                           "count_limit=50000&random=yes&type=1&submissions_per_page=1".format(sid=self.ib_sid, query=query))
        resp = req.json()
        if 'error_code' in resp:
            if resp['error_code'] == 1:
                self.update_ib_sid()
                return self.get_ib(query)
            else:
                raise Exception
        return resp['submissions'][0]


    def call(self, event):
        if event.type != longpoll.VkEventType.MESSAGE_NEW:
            return
        t = event.text.partition(' ')[0] 
        if t not in ('/pony', '/котик', "/рептилия"):
            return
        if t == '/pony':
            random_id_req = requests.get("https://trixiebooru.org/search.json?q=score.gt:200,safe,-animated,-svg,-comic&random_image=1")
            random_id_req.raise_for_status()
            image_id = random_id_req.json()["id"]
            image_req = requests.get("https://trixiebooru.org/%s.json" % image_id)
            image_req.raise_for_status()
            image_json = image_req.json()
            image_url = "https:" + image_json['image']
            image_data_req = requests.get(image_url)
            image_data_req.raise_for_status()
            image_data = io.BytesIO(image_data_req.content)
            vk_response = "https://derpibooru.org/%s\n%s" % (image_id, image_json['source_url'])

        if t in ('/котик', "/рептилия"):
            if t == '/котик':
                resp = self.get_ib('cat')
            if t == '/рептилия':
                resp = self.get_ib('reptile')
            image_data_req = requests.get(resp['file_url_full'])
            image_data_req.raise_for_status()
            image_data = io.BytesIO(image_data_req.content)
            vk_response = "https://inkbunny.net/submissionview.php?id=%s" % (resp['submission_id'])

        vk_upload_resp = self.bot.upload_message_photo([image_data])
        image_vkid = vk_upload_resp[0]['id']
        self.bot.api.messages.send(message=vk_response,
                                     attachment='photo%d_%d' % (self.bot.bot_id, image_vkid),
                                     peer_id=event.peer_id)
