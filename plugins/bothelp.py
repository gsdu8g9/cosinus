import vk

from bot import vkapi

event_id = 4


def call(event):
  if event[0] == event_id:
    if event[6].partition(' ')[0] == '/help' and event[3] < 2000000000:
        emotes = vkapi.photos.get(album_id=228083099)['items']
        respond = []
        respond += ['Список команд:']

        respond += ['''/help - вывод помощи
/анекдот - рассказать несмешной анекдот
/status - аптайм бота
/google [запрос]
/pony - показать картинку с лошадкой
''']  # Пока так

        respond += ['Список эмоций:']
        for emote in emotes:
            respond += [emote['text']]

        try:
            vkapi.messages.send(message='\n'.join(respond), peer_id=event[3])
        except vk.exceptions.VkAPIError as e:
            if e.code != 9:
                raise
