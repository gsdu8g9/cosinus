#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import random
import json
import collections
import time
import requests
import vk

# https://oauth.vk.com/authorize?client_id=5282063&redirect_uri=http://api.vk.com/blank.html&scope=messages,photos&display=page&response_type=token
# Файл token должен содержать токен

vk_token = open('token').read()

session = vk.Session(access_token=vk_token)
vkapi = vk.API(session, v='5.45')

if os.name == 'posix':
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()

random.seed()
start_time = datetime.datetime.now()

schedule = json.loads(open('schedule.json').read())
emotes = vkapi.photos.get(album_id=228083099)['items']

def send_vk_message(msg, attach, uid):
    msg = str(random.random()) + '\n' + msg
    #print(msg)
    vkapi.messages.send(message=msg, attachment=attach, peer_id=uid)

def bot_help(msg):
    respond = 'Список команд:\n'
    for (command, callback) in commands.items():
        respond += command + '\n' 
    
    respond += '\nСписок эмоций:\n'
    for emote in emotes:
        respond += emote + '\n'
        
    return (respond, '')

def bot_status(msg):
    return ('Я жив ' + str(datetime.datetime.now() - start_time), '')

def bot_isin(msg):
    uid = msg['user_id']
    blacklist = [90067990]

    if not (uid in blacklist):
        if (uid == 328822798):
            return ('Можешь посмотреть в зеркало', '')
        else:
            isin = vkapi.photos.get(album_id=227998943)
            rid = random.choice(isin['items'])['id']
            return ("Isin_photo=" + str(rid), 'photo348580470_' + str(rid))

def bot_google(msg):
    body = msg['body']
    
    request_pos = body.find('google ')
    request_pos += len('google ')
    end_of_line = body.find('\n', request_pos)
    
    search_request = body[request_pos:end_of_line].strip()
    search_request = search_request.replace('+', '%2B')
    search_request = search_request.replace('&', '%26')
    search_request = search_request.replace(' ', '+')

    search_url = 'https://www.google.com/search?q=' + search_request
    return (search_url, '')

def bot_schedule(msg):
    current_time = datetime.datetime.now()
    week_number = datetime.datetime.today().isocalendar()[1] % 2
    week_parity = 2 if week_number == 0 else 1

    current_lesson = None
    next_lesson = None

    def get_lesson_time(st):
        t = datetime.datetime.strptime(st, '%H:%M')
        t = t.replace(year=current_time.year, month=current_time.month, day=current_time.day)
        return t


    def print_lesson(lesson):
        lesson_info = 'Предмет: ' + lesson['name'] + '\n' + \
                    'Начало: ' + lesson['start'] + '\n' + \
                    'Окончание: ' + lesson['end'] + '\n' + \
                    'Аудитория: ' + str(lesson['class']) + '\n' + \
                    'Препод: ' + lesson['teacher']
        return lesson_info


    for lesson in schedule[current_time.weekday()]:
        if lesson['week'] == 0 or lesson['week'] == week_parity:
            start = get_lesson_time(lesson['start'])
            end = get_lesson_time(lesson['end'])

            if (current_time > start) and (current_time < end):
                current_lesson = lesson

            if current_time < start:
                next_lesson = lesson
                break

    reply = ''

    if current_lesson is not None:
        reply += 'Текущая пара:\n'
        reply += print_lesson(current_lesson)
        reply += '\n'
    else:
        reply += 'Сейчас пары нет\n'

    if next_lesson is not None:
        reply += 'Следующая пара:\n'
        reply += print_lesson(next_lesson)
        reply += '\n'
    else:
        reply += 'Сегодня больше нет пар\n'

    return (reply, '')

def bot_week(msg):
    week_number = datetime.datetime.today().isocalendar()[1]
    week_parity = "Шла четная неделя ледникового периода... Мы выживали как могли" if (week_number % 2) == 0 else "Нечетная неделя"
    return (week_parity, '')

def bot_python(msg):
    if (random.randint(0, 1) == 0):
        return ('Шшшшш...', 'photo348580470_401471407')
    else:
        return ('Python - лучший язык', '')

def bot_zen(msg):
    zen = '''Красивое лучше, чем уродливое.
Явное лучше, чем неявное.
Простое лучше, чем сложное.
Сложное лучше, чем запутанное.
Плоское лучше, чем вложенное.
Разреженное лучше, чем плотное.
Читаемость имеет значение.
Особые случаи не настолько особые, чтобы нарушать правила.
При этом практичность важнее безупречности.
Ошибки никогда не должны замалчиваться.
Если не замалчиваются явно.
Встретив двусмысленность, отбрось искушение угадать.
Должен существовать один — и, желательно, только один — очевидный способ сделать это.
Хотя он поначалу может быть и не очевиден, если вы не голландец.
Сейчас лучше, чем никогда.
Хотя никогда зачастую лучше, чем прямо сейчас.
Если реализацию сложно объяснить — идея плоха.
Если реализацию легко объяснить — идея, возможно, хороша.
Пространства имён — отличная штука! Будем делать их побольше!'''
    
    return (zen, '')

def bot_matan(msg):
    city = ['Югорск', 'Казахстан', 'Петербург', 'МСГ']
    photos = ['photo87425516_406709633', 'photo24524121_389966755', 'photo22195634_374008826']
    action = ['конину', 'кумыса', 'учиться', 'погулять', 'на посвят в восьмерку', 'на допсу по физике', 'на допсу по матану', 'научиться кодить', 'в общагу', 'сдать матан']
    action2 = ['стать богом', 'стать йогом', 'сбежать из дома', 'пойти на концерт Алисы', 'надеть колпак', 'выучить матан', 'поступить в ЛЭТИ', 'стать зав.кафедры ВМ']

    return ('В небольшом селе ' + random.choice(city) + ' жил был маленький мальчик Андрюша.\nЗахотел как-то Андрюша ' + random.choice(action) + ', но мамка не разрешила :C\n' +\
            'И тогда решил Андрюшка ' + random.choice(action2) + ' и ' + random.choice(action2) + '.\n'\
            'Больше его никто не видел.', random.choice(photos))

commands = collections.OrderedDict([
    ('/help', bot_help),
    ('/status', bot_status),
    ('/random', None),

    ('/Isin, !Женя', bot_isin),
    ('/google [запрос]', bot_google),
    ('/пары', bot_schedule),
    ('/неделя', bot_week),
    ('/python', bot_python),
    ('/дзен', bot_zen),
    ('/матан', bot_matan)])

# главный цикл
b = True
while True:
    try:
        longpoll = vkapi.messages.getLongPollServer(need_pts=1, use_ssl=0)
        ts = longpoll['ts']
        pts = 0
        if b:
            pts = longpoll['pts']
            b = False
        else:
            time.sleep(3)
            pts = newpts['new_pts']

        newpts = vkapi.messages.getLongPollHistory(pts=pts, ts=ts, fields='')

        for msg in newpts['messages']['items']:
            if msg['out'] == 0:
                if 'chat_id' in msg:
                    uid = 2000000000 + msg['chat_id']
                else:
                    uid = msg['user_id']

                respond = ''
                attachment = ''

                # команды
                for cmd in commands:
                    if (cmd in msg['body']) and (commands[cmd] is not None):
                        r = commands[cmd](msg)

                        if (respond != ''):
                            respond += '\n'
                        respond += r[0]

                        if (attachment != ''):
                            attachment += '\n'
                        attachment += r[1]


                # эмоции
                for emote in emotes:
                    if ((emote['text'] + ' ') in msg['body']) or \
                       ((emote['text'] + '\n') in msg['body']) or \
                       (msg['body'].find(emote['text']) + len(emote) == len(msg['body'])):
                        if (attachment != ''):
                            attachment += ','
                        attachment += 'photo348580470_' + emote['id']


                send_vk_message(respond, attachment, uid)


    except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError, vk.exceptions.VkAPIError) as e:
#        print('Fuck!')
        print(e)
