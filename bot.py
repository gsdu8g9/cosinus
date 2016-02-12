#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import random
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

start_time = datetime.datetime.now()

schedule = [
    # ПН
    [{'name': 'Физ-ра',
      'week': 0,
      'start': '8:00',
      'end': '9:30',
      'class': 0,
      'teacher': '-'},

     {'name': 'Матан (лекц)',
      'week': 0,
      'start': '9:50',
      'end': '11:20',
      'class': 3308,
      'teacher': 'Солнышкин Сергей Николаевич'},

     {'name': 'Дискретная математика (пр)',
      'week': 0,
      'start': '11:40',
      'end': '13:10',
      'class': 2114,
      'teacher': 'Чухнов Антон Сергеевич'}],

    # ВТ
    [{'name': 'Экономика (пр)',
      'week': 2,
      'start': '11:40',
      'end': '13:10',
      'class': 3426,
      'teacher': 'Заставенко Екатерина Валерьевна'},

     {'name': 'АиГ (лекц)',
      'week': 0,
      'start': '13:45',
      'end': '15:15',
      'class': 3308,
      'teacher': 'Зельвенский Игорь Григорьевич'},

     {'name': 'Матан (пр)',
      'week': 0,
      'start': '15:35',
      'end': '17:05',
      'class': 3313,
      'teacher': 'Коточигов Александр Михайлович'},

     {'name': 'АиГ (лекц)',
      'week': 0,
      'start': '17:25',
      'end': '18:55',
      'class': 3428,
      'teacher': 'Зельвенский Игорь Григорьевич'}],

    # СР
    [{'name': 'Экономика (лекц)',
      'week': 1,
      'start': '8:00',
      'end': '9:30',
      'class': 5405,
      'teacher': 'Ягья Талие Саидовна'},

     {'name': 'Англ.яз.',
      'week': 0,
      'start': '9:55',
      'end': '11:20',
      'class': 0,
      'teacher': '-'},

     {'name': 'Физика (лекц)',
      'week': 0,
      'start': '11:40',
      'end': '13:10',
      'class': 3107,
      'teacher': 'Шейнман Илья Львович'},

     {'name': 'Физ-ра',
      'week': 0,
      'start': '13:45',
      'end': '15:15',
      'class': 0,
      'teacher': '-'}],

    # ЧТ
    [{'name': 'История (лекц)',
      'week': 1,
      'start': '13:45',
      'end': '15:15',
      'class': 5423,
      'teacher': 'Меньшиков Дмитрий Никитович'},

     {'name': 'Физ-ра',
      'week': 2,
      'start': '13:45',
      'end': '15:15',
      'class': 0,
      'teacher': '-'},

     {'name': 'Программирование (лекц)',
      'week': 0,
      'start': '15:35',
      'end': '17:05',
      'class': 5405,
      'teacher': 'Самойленко Владимир Петрович'},

     {'name': 'Программирование',
      'week': 1,
      'start': '17:25',
      'end': '18:55',
      'class': 3402,
      'teacher': 'Самойленко Владимир Петрович'}],

    # ПТ
    [],

    # СБ
    [{'name': 'История',
      'week': 0,
      'start': '11:40',
      'end': '13:10',
      'class': 3417,
      'teacher': 'Стогов Дмитрий Игоревич'},

     {'name': 'Дискретная математика (лекц)',
      'week': 0,
      'start': '13:45',
      'end': '15:15',
      'class': 3308,
      'teacher': 'Рыбин Сергей Витальевич'},

     {'name': 'Физика (пр)',
      'week': 1,
      'start': '15:35',
      'end': '17:05',
      'class': 3107,
      'teacher': 'Морозов Вениамин Васильевич'},

     {'name': 'Физика (лаб)',
      'week': 2,
      'start': '15:35',
      'end': '17:05',
      'class': 0,
      'teacher': 'Иманбаева Райхан Талгатовна, Демидов Юрий Андреевич'}]]

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
                    rec = 2000000000 + msg['chat_id']
                else:
                    rec = msg['user_id']

                if msg['body'] == 'random':
                    vkapi.messages.send(message=str(random.random()), peer_id=rec)
                elif ('chat_id' not in msg) and (msg['body'] == 'help'):
                    reply = str(random.random()) + '''\nДоступные команды:
                    ЛС: help random status
                    Чат и ЛС: Kappa FeelsGoodMan FeelsBadMan Kreygasm PogChamp BibleThump BestPony
                              (Isin Женя) Пары
                              google'''
                    vkapi.messages.send(message=reply, peer_id=rec)
                elif msg['body'] == 'Kappa':
                    vkapi.messages.send(message="Kappa " + str(random.random()),
                                        attachment='photo348580470_401578683', peer_id=rec)
                elif msg['body'] == 'status':
                    vkapi.messages.send(message="Я жив " + str(datetime.datetime.now() - start_time), peer_id=rec)
                elif msg['body'] == 'FeelsGoodMan':
                    vkapi.messages.send(message="FeelsGoodMan " + str(random.random()),
                                        attachment='photo348580470_401638534', peer_id=rec)
                elif msg['body'] == 'FeelsBadMan':
                    vkapi.messages.send(message="FeelsBadMan " + str(random.random()),
                                        attachment='photo348580470_401822965', peer_id=rec)
                elif msg['body'] == 'Kreygasm':
                    vkapi.messages.send(message="Kreygasm " + str(random.random()),
                                        attachment='photo348580470_401822961', peer_id=rec)
                elif msg['body'] == 'PogChamp':
                    vkapi.messages.send(message="PogChamp  " + str(random.random()),
                                        attachment='photo348580470_401822959', peer_id=rec)
                elif msg['body'] == 'BibleThump':
                    vkapi.messages.send(message="BibleThump " + str(random.random()),
                                        attachment='photo348580470_401822963', peer_id=rec)
                elif msg['body'].startswith('google '):
                    search_request = msg['body'][7:].strip()
                    search_request = search_request.replace('+', '%2B')
                    search_request = search_request.replace('&', '%26')
                    search_request = search_request.replace(' ', '+')
                    search_url = 'https://www.google.com/search?q=' + search_request
                    vkapi.messages.send(message=search_url, peer_id=rec)
                elif msg['body'] == 'Женя' or msg['body'] == 'Isin':
                    if msg['user_id'] == 90067990:
                        pass
                    elif msg['user_id'] == 328822798:
                        vkapi.messages.send(message="Можешь посмотреть в зеркало", peer_id=rec)
                    else:
                        zhenya = vkapi.photos.get(album_id=227998943)
                        rid = random.choice(zhenya['items'])['id']
                        vkapi.messages.send(message="Photo " + str(rid),
                                            attachment='photo348580470_' + str(rid), peer_id=rec)
                elif msg['body'] == "Пары":
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

                    vkapi.messages.send(message=reply, peer_id=rec)


    except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError, vk.exceptions.VkAPIError) as e:
        #    print('Fuck!')
        print(e)
