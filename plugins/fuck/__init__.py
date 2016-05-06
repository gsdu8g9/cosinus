import io
from PIL import Image, ImageDraw, ImageOps
import os
import requests
import vk

from bot import vkapi, bot_id

event_id = 4


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
    gestured_image = io.BytesIO(gestured_image.getvalue())

    return gestured_image


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
    if event[6] != '/gesture':
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
        gestured_image = draw_gesture(image)

        # загружаем это дело на сервак
        image_id = upload_image(gestured_image)

        # добавляем картинку в ответное сообщение

        attach += ['photo' + str(bot_id) + '_' + str(image_id)]

    attach = ','.join(attach)

    try:
        vkapi.messages.send(message="", attachment=attach, peer_id=event[3])
    except vk.exceptions.VkAPIError as e:
        if e.code != 9:
            raise
