import io
from PIL import Image
import os
import requests
import vk
import numpy

from bot import AbstractChatPlugin


def draw_picture(img_src):
    fap_path = os.path.join(os.path.dirname(__file__), "fap.png")

    # подгружаем картинку
    response = requests.get(img_src)
    response.raise_for_status()
    image_bytes = io.BytesIO(response.content)

    # открываем
    image = Image.open(image_bytes)
    fap_pic = Image.open(fap_path)

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    image_width, image_height = image.size
    fap_width, fap_height = fap_pic.size

    def find_coeffs(pa, pb):
        """ https://stackoverflow.com/questions/14177744/
            Здесь твориться дичь, имя которой - алгебра
            """
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
        A = numpy.matrix(matrix, dtype=numpy.float)
        B = numpy.array(pb).reshape(8)
        res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        return numpy.array(res).reshape(8)

    trans_coeff = find_coeffs(
        [(217,111),(412,115),(222,372),(403,371)],
        [(0,0), (image_width-1,0), (0,image_height-1), (image_width-1, image_height-1)])

    resp_pic = image.transform(fap_pic.size, Image.PERSPECTIVE, trans_coeff, Image.BILINEAR)

    # прикрепляем gesture к image
    resp_bytes = io.BytesIO()
    Image.alpha_composite(resp_pic, fap_pic).save(resp_bytes, format='PNG')
    resp_bytes.seek(0)

    return resp_bytes


class ChatPlugin(AbstractChatPlugin):
    help = '''/fap [картинка] - пририсовать прикрепленную картинку в картинку с ноутбуком и чьей-то рукой'''

    def call(self, event):
        if event[0] != 4:
            return

        if event[6] != '/fap':
            return

        try:
            attachments = event[7]
        except IndexError:
            return

        # Дай бог здоровья девелоперам из мэилру
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
            pic = draw_picture(image)

            # загружаем это дело на сервак
            image_id = self.bot.upload_message_image(pic)[0]['id']

            # добавляем картинку в ответное сообщение

            attach.add('photo%d_%d' % (self.bot.bot_id, image_id))

        attach = ','.join(attach)

        try:
            self.bot.vkapi.messages.send(message="", attachment=attach, peer_id=event[3])
        except vk.exceptions.VkAPIError as e:
            if e.code != 9:
                raise
