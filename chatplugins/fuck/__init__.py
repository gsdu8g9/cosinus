import io
from PIL import Image, ImageOps
import os
import requests
import vk

from bot import AbstractChatPlugin


def draw_gesture(img_src):
    gesture_path = os.path.join(os.path.dirname(__file__), "gesture.png")

    # подгружаем картинку
    response = requests.get(img_src)
    response.raise_for_status()
    image_bytes = io.BytesIO(response.content)

    # открываем
    image = Image.open(image_bytes)
    gesture = Image.open(gesture_path)

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    if gesture.mode != 'RGBA':
        gesture = gesture.convert('RGBA')

    # подгоняем размер gesture под image
    image_width, image_height = image.size
    gest_width, gest_height = gesture.size

    k = 2 / 3
    if (image_width / image_height) < (gest_width / gest_height):
        new_width = k * image_width
        new_height = new_width / gest_width * gest_height
    else:
        new_height = k * image_height
        new_width = new_height / gest_height * gest_width

    gesture = gesture.resize((int(new_width), int(new_height)))
    gest_width, gest_height = gesture.size
    diff0 = image_width - gest_width
    diff1 = image_height - gest_height
    gesture = ImageOps.expand(gesture, border=(diff0, diff1, 0, 0), fill=0)

    # прикрепляем gesture к image
    gestured_image = io.BytesIO()
    Image.alpha_composite(image, gesture).save(gestured_image, format='PNG')
    # Хрен знает, как это делается правильно
    gestured_image.seek(0)

    return gestured_image


class ChatPlugin(AbstractChatPlugin):
    help = '''/gesture [картинка] - пририсовать к картинке средний палец одного из создателей бота'''

    def call(self, event):
        if event[0] != 4:
            return

        # А lazy-evaluation нам не завезли
        if event[6] != '/gesture':
            return

        try:
            attachments = event[7]
        except IndexError:
            return

        photo_attachments = set()
        d = 1
        while(1):
            try:
                attach_type = attachments["attach%d_type" % d]
            except KeyError:
                break
            if attach_type == "photo":
                photo_attachments.add(attachments["attach%d" % d])
            d += 1
        if not photo_attachments:
            return

        self.bot.vkapi.messages.setActivity(type='typing', peer_id=event[3])

        photos = self.bot.vkapi.photos.getById(photos=','.join(photo_attachments))

        photo_sizes = [2560, 1280, 807, 604, 130, 75]  # Не использовать set
        photo_srcs = set()
        for photo in photos:
            for size in photo_sizes:
                try:
                    photo_srcs.add(photo['photo_' + str(size)])
                    break
                except KeyError:
                    continue

        attach = set()

        for image in photo_srcs:
            # собственно, пририсовываем фак
            gestured_image = draw_gesture(image)

            # загружаем это дело на сервак
            image_id = self.bot.upload_message_image(gestured_image)[0]['id']

            # добавляем картинку в ответное сообщение

            attach.add('photo%d_%d' % (self.bot.bot_id, image_id))

        attach = ','.join(attach)

        try:
            self.bot.vkapi.messages.send(message="", attachment=attach, peer_id=event[3])
        except vk.exceptions.VkAPIError as e:
            if e.code != 9:
                raise
