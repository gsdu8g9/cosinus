#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import datetime
import json
import os
import random
import re
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

schedule = json.load(open('schedule.json',encoding='utf8'))
emotes = vkapi.photos.get(album_id=228083099)['items']

random.seed()
start_time = datetime.datetime.now()


# def send_vk_message(msg, attach, uid):
#     msg = str(random.random()) + '\n' + msg
#     # print(msg)
#     vkapi.messages.send(message=msg, attachment=attach, peer_id=uid)


def bot_help(msg,uid):
    if uid <= 2000000000:
        respond = 'Список команд:\n'
        for (command, callback) in commands.items():
            respond += command + '\n'

        respond += '\nСписок эмоций:\n'
        for emote in emotes:
            respond += emote['text'] + '\n'

        vkapi.messages.send(message=respond, peer_id=uid)


def bot_status(msg,uid):
    if uid <= 2000000000:
        r = 'Я жив ' + str(datetime.datetime.now() - start_time)
        vkapi.messages.send(message=r, peer_id=uid)


def bot_isin(msg,uid):
    blacklist = [90067990]
    if not (msg['user_id'] in blacklist):
        if msg['user_id'] == 328822798:
            r = 'Можешь посмотреть в зеркало'
            a = ''
        else:
            isin = vkapi.photos.get(album_id=227998943)
            rid = random.choice(isin['items'])['id']
            r = "Isin_photo=" + str(rid)
            a = 'photo348580470_' + str(rid)
    vkapi.messages.send(message=r, attachment=a, peer_id=uid)


def bot_google(msg,uid):
    search_request = msg['body'].partition(' ')[2].partition('\n')[0]
    search_request = search_request.replace('+', '%2B')
    search_request = search_request.replace('&', '%26')
    search_request = search_request.replace(' ', '+')
    search_url = 'https://www.google.com/search?q=' + search_request
    vkapi.messages.send(message=search_url, peer_id=uid)


def bot_schedule(msg,uid):
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

    vkapi.messages.send(message=reply, peer_id=uid)


def bot_week(msg,uid):
    week_number = datetime.datetime.today().isocalendar()[1]
    week_parity = "Шла четная неделя ледникового периода... Мы выживали как могли" if (week_number % 2) == 0 else "Нечетная неделя"
    vkapi.messages.send(message=week_parity, peer_id=uid)


def bot_python(msg,uid):
    if random.randint(0, 1) == 0:
        r = 'Шшшшш...'
        a = 'photo348580470_401471407'
    else:
        r = 'Python - лучший язык'
        a = ''
    vkapi.messages.send(message=r, attachment=a, peer_id=uid)


def bot_random(msg,uid):
    vkapi.messages.send(message=random.random(), peer_id=uid)


def bot_zen(msg,uid):
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

    vkapi.messages.send(message=zen, peer_id=uid)


def bot_matan(msg,uid):
    city = ['Югорск', 'Казахстан', 'Петербург', 'МСГ']
    photos = ['photo87425516_406709633', 'photo24524121_389966755', 'photo22195634_374008826']
    action = ['конину', 'кумыса', 'учиться', 'погулять', 'на посвят в восьмерку', 'на допсу по физике',
              'на допсу по матану', 'научиться кодить', 'в общагу', 'сдать матан']
    action2 = ['стать богом', 'стать йогом', 'сбежать из дома', 'пойти на концерт Алисы', 'надеть колпак',
               'выучить матан', 'поступить в ЛЭТИ', 'стать зав.кафедры ВМ']

    story = 'В небольшом селе ' + random.choice(city) + ' жил был маленький мальчик Андрюша.\n' \
            'Захотел как-то Андрюша ' + random.choice(action) + ', но мамка не разрешила :C\n' \
            'И тогда решил Андрюшка ' + random.choice(action2) + ' и ' + random.choice(action2) + '.\n' \
            'Больше его никто не видел.'

    vkapi.messages.send(message=story, attachment=random.choice(photos), peer_id=uid)


commands = collections.OrderedDict([
    ('/help', bot_help),
    ('/status', bot_status),
    ('/random', bot_random),
    ('/Isin', bot_isin),
    ('/google', bot_google),
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

                # команды
                for cmd in commands:
                    if (cmd == msg['body'].partition(' ')[0]):
                        commands[cmd](msg,uid)
                        break

                # эмоции
                else:
                    attachments = ''
                    for emote in emotes:
                        if re.compile(r'\b({0})\b'.format(emote['text'])).search(msg['body']) is not None:
                            if attachments != '':
                                attachments += ','
                            attachments += 'photo348580470_' + str(emote['id'])
                    if attachments != '':
                        vkapi.messages.send(message=str(random.random()), attachment=attachments, peer_id=uid)


    except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError, vk.exceptions.VkAPIError) as e:
        #        print('Fuck!')
        print(e)
