import io
from random import randint

import requests

import longpoll


class Plugin:
    help = """/pony - присылает в ответ случайную картинку с поняшкой, /котик - c котиком"""

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("pone", self.call)

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
                image_id = randint(1, 1500)
                image_req = requests.get("https://e926.net/post/index.json?page=%d&tags=cat order:score -meme type:jpg type:png&limit=1" % image_id)
            if t == '/рептилия':
                image_id = randint(1, 1500)
                image_req = requests.get("https://e926.net/post/index.json?page=%d&tags=reptile order:score -meme type:jpg type:png&limit=1" % image_id)
            image_req.raise_for_status()
            image_json = image_req.json()[0]
            image_url = image_json['file_url']
            image_data_req = requests.get(image_url)
            image_data_req.raise_for_status()
            image_data = io.BytesIO(image_data_req.content)
            vk_response = "https://e926.net/post/show/%d\n%s" % (image_json['id'], image_json['source'])

        vk_upload_resp = self.bot.upload_message_photo([image_data])
        image_vkid = vk_upload_resp[0]['id']
        self.bot.api.messages.send(message=vk_response,
                                     attachment='photo%d_%d' % (self.bot.bot_id, image_vkid),
                                     peer_id=event.peer_id)
