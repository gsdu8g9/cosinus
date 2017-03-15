import longpoll
from gtts import gTTS
import io


class Plugin:
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_longpoll_parser("gtts", self.call)

    def call(self, event):
        if (event.type == longpoll.VkEventType.MESSAGE_NEW
                and event.text.partition(' ')[0] == '/gtts'):
            lang, _, text = event.text.partition(' ')[2].partition(' ')
            tts = gTTS(text=text, lang=lang)
            tts_data = io.BytesIO()
            tts.write_to_fp(tts_data)
            vk_upload_resp = self.bot.upload_audio([tts_data])
            audio_vkid = vk_upload_resp[0]['id']
            self.bot.api.messages.send(attachment='audio%d_%d' % (self.bot.bot_id, audio_vkid),
                                       peer_id=event.peer_id)
