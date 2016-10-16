import io

import requests

from bot import AbstractChatPlugin


class ChatPlugin(AbstractChatPlugin):
    help = """/pony - присылает в ответ случайную картинку с поняшкой"""

    booru = "trixiebooru.org"
    search_string = "score.gt:200,safe,-animated,-svg,-comic"

    def call(self, event):
        if event[0] != 4:
            return
        if event[6].partition(' ')[0] == '/pony':
            random_id_req = requests.get("https://%s/search.json?q=%s&random_image=1" % (self.booru, self.search_string))
            random_id_req.raise_for_status()
            image_id = random_id_req.json()["id"]
            image_req = requests.get("https://%s/%s.json" % (self.booru, image_id))
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
