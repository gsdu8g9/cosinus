import io

from gtts import gTTS
from pydub import AudioSegment

import longpoll


class Plugin:

    silence3 = AudioSegment.silent(duration=3000)

    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("gtts", self.call)

    def call(self, event):
        if (event.type == longpoll.VkEventType.MESSAGE_NEW
                and event.text.partition(' ')[0] == '/tts'):
            lang, _, text = event.text.partition(' ')[2].partition(' ')
            tts = gTTS(text=text, lang=lang)
            tts_data = io.BytesIO()
            tts.write_to_fp(tts_data)
            tts_data.seek(0)
            aseg = AudioSegment.from_mp3(tts_data)
            tts_data.seek(0)
            aseg += self.silence3
            aseg.export(tts_data, format="mp3", tags={"artist": "ГуглТётка", "title": "Сообщение"})
            vk_upload_resp = self.bot.upload_audio(tts_data)
            audio_vkid = vk_upload_resp['id']
            self.bot.api.messages.send(attachment='audio%d_%d' % (self.bot.bot_id, audio_vkid),
                                       peer_id=event.peer_id)
