import io
from random import randint

import requests

from bot import AbstractChatPlugin


class ChatPlugin(AbstractChatPlugin):
    help = """/pony - присылает в ответ случайную картинку с поняшкой, /котик - c котиком"""

    def call(self, event):
        if event[0] != 4:
            return
        if event[6].partition(' ')[0] == '/pony':
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

            vk_upload_resp = self.bot.upload_message_image(image_data)

            image_vkid = vk_upload_resp[0]['id']

            vk_response = "https://derpibooru.org/%s\n%s" % (image_id, image_json['source_url'])

            self.bot.vkapi.messages.send(message=vk_response,
                                         attachment='photo%d_%d' % (self.bot.bot_id, image_vkid),
                                         peer_id=event[3])

        if event[6].partition(' ')[0] in ('/котик', "/рептилия"):
            if event[6].partition(' ')[0] == '/котик':
                image_id = randint(1, 1500)
                image_req = requests.get("https://e926.net/post/index.json?page=%d&tags=cat order:score -meme type:jpg type:png&limit=1" % image_id)
            if event[6].partition(' ')[0] == '/рептилия':
                image_id = randint(1, 1500)
                image_req = requests.get("https://e926.net/post/index.json?page=%d&tags=reptile order:score -meme type:jpg type:png&limit=1" % image_id)
            image_req.raise_for_status()
            image_json = image_req.json()[0]
            image_url = image_json['file_url']
            image_data_req = requests.get(image_url)
            image_data_req.raise_for_status()
            image_data = io.BytesIO(image_data_req.content)

            vk_upload_resp = self.bot.upload_message_image(image_data)
            image_vkid = vk_upload_resp[0]['id']

            vk_response = "https://e926.net/post/show/%d\n%s" % (image_json['id'], image_json['source'])
            self.bot.vkapi.messages.send(message=vk_response,
                                         attachment='photo%d_%d' % (self.bot.bot_id, image_vkid),
                                         peer_id=event[3])
