import io
import os
import lxml.html
import subprocess

import requests
import youtube_dl

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
        if t not in ('/pony', '/котик', "/рептилия", "/лайвкоты"):
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
        elif t == '/рептилия':
            resp = self.get_ib('reptile')
            image_data_req = requests.get(resp['file_url_full'])
            image_data_req.raise_for_status()
            image_data = io.BytesIO(image_data_req.content)
            vk_response = "https://inkbunny.net/submissionview.php?id=%s" % (resp['submission_id'])
        elif t == '/котик':
            catpage = requests.get("http://mimimi.ru/random")
            catpage.raise_for_status()
            cattree = lxml.html.fromstring(catpage.text)
            catelem = cattree.xpath('''//div[@class="mi-image"]/*/img''')[0]
            catimgsrc = catelem.attrib['src']
            catdatareq = requests.get(catimgsrc)
            catdatareq.raise_for_status()
            image_data = io.BytesIO(catdatareq.content)
            vk_response = "http://mimimi.ru/"
        elif t == '/лайвкоты':
            mew_url = youtube_dl.YoutubeDL({"quiet": True}).extract_info("7-gwjv1WhYM", download=False)['url']
            mew_ffp = subprocess.run(
                '''ffmpeg -i {} -vframes 1 -c:v mjpeg -q:v 4 -f image2 pipe:1'''.format(mew_url),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
            image_data = io.BytesIO(mew_ffp.stdout)
            vk_response = "https://www.youtube.com/watch?v=7-gwjv1WhYM"

        vk_upload_resp = self.bot.upload_message_photo([image_data])
        image_vkid = vk_upload_resp[0]['id']
        self.bot.api.messages.send(message=vk_response,
                                     attachment='photo%d_%d' % (self.bot.bot_id, image_vkid),
                                     peer_id=event.peer_id)
