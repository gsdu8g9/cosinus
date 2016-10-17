from bot import AbstractChatPlugin
import requests


class ChatPlugin(AbstractChatPlugin):
    def call(self, event):
        if event[0] != 4:
            return
        if event[6] != '/emo':
            return
        try:
            event[7]
        except IndexError:
            return

        msg = self.bot.vkapi.messages.getById(message_ids=event[1])['items'][0]

        self.bot.vkapi.messages.setActivity(type='typing', peer_id=event[3])

        photo_src = None
        photo_sizes = (2560, 1280, 807, 604, 130, 75)

        for attachment in msg['attachments']:
            try:
                photo = attachment['photo']
            except KeyError:
                continue
            # выбираем наибольшее доступное изображение
            for size in photo_sizes:
                try:
                    photo_src = photo['photo_' + str(size)]
                    break
                except KeyError:
                    continue
            if photo_src:
                break

        self.bot.vkapi.messages.setActivity(type='typing', peer_id=event[3])

        req = requests.post("https://api.projectoxford.ai/emotion/v1.0/recognize",
                            headers={
                                'Ocp-Apim-Subscription-Key': self.bot.config["microsoft-cognitive"]["emotion-key"],
                                'Content-Type': 'application/json'
                            },
                            json={"url": photo_src})

        if req.status_code in (403, 429):
            vk_response = "Превышен лимит запросов"

        if req.status_code == 200:
            resp = req.json()
            if len(resp) == 0:
                vk_response = "Лиц на фотографии не найдено"
            else:
                vk_response = []
                if len(resp) > 1:
                    d = 1
                else:
                    d = 0
                for face in resp:
                    scores = {k: v * 100 for (k, v) in face['scores'].items()}
                    if d:
                        vk_response.append("Лицо %d:" % d)
                    vk_response.append("Злость: %0.2f%%" % scores['anger'])
                    vk_response.append("Презрение: %0.2f%%" % scores['contempt'])
                    vk_response.append("Отвращение: %0.2f%%" % scores['disgust'])
                    vk_response.append("Страх: %0.2f%%" % scores['fear'])
                    vk_response.append("Счастье: %0.2f%%" % scores['happiness'])
                    vk_response.append("Нейтральность: %0.2f%%" % scores['neutral'])
                    vk_response.append("Печаль: %0.2f%%" % scores['sadness'])
                    vk_response.append("Удивление: %0.2f%%" % scores['surprise'])
                    d += 1

        self.bot.vkapi.messages.send(message='\n'.join(vk_response), peer_id=event[3])
