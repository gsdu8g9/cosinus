# -*- coding: utf-8 -*-
import random
import io

from gtts import gTTS
from pydub import AudioSegment

import longpoll
from .anecs import anecs


class Plugin:

    silence3 = AudioSegment.silent(duration=3000)

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("anecs_text", self.call_text)
        self.bot.add_longpoll_parser("anecs_voice", self.call_voice)

    help = '''/анекдот - рассказать очень смешной анекдот'''

    def call_text(self, event):
        if event.type != longpoll.VkEventType.MESSAGE_NEW:
            return
        if event.text.partition(' ')[0] == '/анекдот':
            try:
                n = int(event.text.partition(' ')[2])
                if not (0 < n <= len(anecs)):
                    raise ValueError()
            except ValueError:
                n = random.randint(1, len(anecs) + 1)
            self.bot.api.messages.send(message='Анекдот %d\n%s' % (n, anecs[n - 1]), peer_id=event.peer_id)

    def call_voice(self, event):
        if event.type != longpoll.VkEventType.MESSAGE_NEW:
            return
        if event.text.partition(' ')[0] == '/tts-анекдот':
            try:
                n = int(event.text.partition(' ')[2])
                if not (0 < n <= len(anecs)):
                    raise ValueError()
            except ValueError:
                n = random.randint(1, len(anecs) + 1)
            tts = gTTS(text=anecs[n - 1], lang="ru")
            tts_data = io.BytesIO()
            tts.write_to_fp(tts_data)
            tts_data.seek(0)
            aseg = AudioSegment.from_mp3(tts_data)
            tts_data.seek(0)
            aseg += self.silence3
            aseg.export(tts_data, format="mp3", tags={"artist": "ГуглТётка", "title": "Анекдот %d" % n})
            vk_upload_resp = self.bot.upload_audio(tts_data)
            audio_vkid = vk_upload_resp['id']
            self.bot.api.messages.send(attachment='audio%d_%d' % (self.bot.bot_id, audio_vkid),
                                       peer_id=event.peer_id)
