import io
from PIL import Image, ImageDraw, ImageOps
import os
import requests
import vk
import numpy

from bot import vkapi, bot_id

event_id = 4

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
        [(0,0), (image_width-1,0),(0,image_height-1), (image_width-1, image_height-1)])

    resp_pic = image.transform(fap_pic.size,Image.PERSPECTIVE,trans_coeff,Image.BILINEAR)

    # прикрепляем gesture к image
    resp_bytes = io.BytesIO()
    Image.alpha_composite(resp_pic,fap_pic).save(resp_bytes, format='PNG')
    # Хрен знает, как это делается правильно
    resp_bytes = io.BytesIO(resp_bytes.getvalue())

    return resp_bytes

def upload_image(image):
    f = {'photo': ('image.png', image, 'image/png')}
    upload_server = vkapi.photos.getMessagesUploadServer()
    upload_url = upload_server['upload_url']

    # отправляем
    send_response = requests.post(upload_url, files=f)

    # сохраняем
    save_response = vkapi.photos.saveMessagesPhoto(**send_response.json())

    image_id = save_response[0]['id']
    return image_id

def call(event):
    if event[6] != '/fap':
        return

    vkapi.messages.setActivity(type='typing',peer_id=event[3])

    msg_id = event[1]
    msg = vkapi.messages.getById(message_ids=msg_id)['items'][0]

    photo_sizes = [2560, 1280, 807, 604, 130, 75]

    # проверяем, что вложения действительно есть
    if 'attachments' not in msg:
        return

    attachments = msg['attachments']

    # здесь будет хранить url всех найденных картинок
    images_src = []

    for attachment in attachments:
        if attachment['type'] == 'photo':
            photo = attachment['photo']
            # выбираем наибольшее доступное изображение
            for size in photo_sizes:
                if ('photo_' + str(size)) in photo:
                    images_src.append(photo['photo_' + str(size)])
                    break


    attach = []

    for image in images_src:
        # собственно, пририсовываем фак
        pic = draw_picture(image)

        # загружаем это дело на сервак
        image_id = upload_image(pic)

        # добавляем картинку в ответное сообщение

        attach += ['photo' + str(bot_id) + '_' + str(image_id)]

    attach = ','.join(attach)

    try:
        vkapi.messages.send(message="", attachment=attach, peer_id=event[3])
    except vk.exceptions.VkAPIError as e:
        if e.code != 9:
            raise
