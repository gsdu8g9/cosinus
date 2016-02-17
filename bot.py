#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

vk_token = open('token').read().strip()

session = vk.Session(access_token=vk_token)
vkapi = vk.API(session, v='5.45')

if os.name == 'posix':
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()

schedule = json.load(open('schedule.json', encoding='utf8'))
anec = json.load(open('anec.json', encoding='utf8'))

random.seed()
start_time = datetime.datetime.now()

# def send_vk_message(msg, attach, uid):
#     msg = str(random.random()) + '\n' + msg
#     # print(msg)
#     vkapi.messages.send(message=msg, attachment=attach, peer_id=uid)

def is_chat(msg):
    return 'chat_id' in msg


def msg_command(msg):
    return msg['body'].partition(' ')[0]


def bot_help(msg):
    """/help - вывод помощи"""
    if msg_command(msg) == '/help' and not is_chat(msg):
        emotes = vkapi.photos.get(album_id=228083099)['items']
        respond = []  # ОПТИМИЗАЦИЯ, БЛИН
        respond += ['Список команд:\n']

        for command in commands:
            if command.__doc__ is not None:
                respond += [command.__doc__, '\n']

        respond += ['\nСписок эмоций:\n']
        for emote in emotes:
            respond += [emote['text'], '\n']

        return {'message': ''.join(respond)}


def bot_status(msg):
    """/status - аптайм бота"""
    if msg_command(msg) == '/status' and not is_chat(msg):
        r = 'Я жив ' + str(datetime.datetime.now() - start_time)
        return {'message': r}


def bot_isin(msg):
    """/Isin"""
    blacklist = []
    if msg_command(msg) == '/Isin' or re.compile(r'\b(Женя)\b').search(msg['body']) is not None:
        if not (msg['user_id'] in blacklist):
            if msg['user_id'] == 328822798:
                r = 'Можешь посмотреть в зеркало'
                a = ''
            else:
                isin = vkapi.photos.get(album_id=227998943)
                rid = random.choice(isin['items'])['id']
                r = "Isin_photo=" + str(rid)
                a = 'photo348580470_' + str(rid)
            return {'message': r, 'attachment': a}
        else:
            return True


def bot_anec(msg):
    """/анекдот"""
    if msg_command(msg) == '/анекдот':
        return {'message': random.choice(anec)}


def bot_google(msg):
    """/google [запрос]"""
    if msg_command(msg) == '/google':
        search_request = msg['body'].partition(' ')[2].partition('\n')[0]
        search_request = search_request.replace('+', '%2B')
        search_request = search_request.replace('&', '%26')
        search_request = search_request.replace(' ', '+')
        search_url = 'https://www.google.com/search?q=' + search_request
        return {'message': search_url}


def bot_schedule(msg):
    """/пары - вывод текущей и следующей пар для группы 5383 ЛЭТИ"""
    if msg_command(msg) == '/пары':
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
            lesson_info = ['Предмет: ', lesson['name'], '\n',
                           'Начало: ', lesson['start'], '\n',
                           'Окончание: ', lesson['end'], '\n',
                           'Аудитория: ', lesson['class'], '\n',
                           'Препод: ', lesson['teacher']]
            return ''.join(lesson_info)

        for lesson in schedule[current_time.weekday()]:
            if lesson['week'] == 0 or lesson['week'] == week_parity:
                start = get_lesson_time(lesson['start'])
                end = get_lesson_time(lesson['end'])

                if (current_time > start) and (current_time < end):
                    current_lesson = lesson

                if current_time < start:
                    next_lesson = lesson
                    break

        reply = []

        if current_lesson is not None:
            reply += ['Текущая пара:']
            reply += [print_lesson(current_lesson)]
        else:
            reply += ['Сейчас пары нет']

        if next_lesson is not None:
            reply += ['Следующая пара:']
            reply += [print_lesson(next_lesson)]
        else:
            reply += ['Сегодня больше нет пар']

        return {'message': '\n'.join(reply)}


def bot_week(msg):
    """/неделя"""
    if msg_command(msg) == '/неделя':
        week_number = datetime.datetime.today().isocalendar()[1]
        week_parity = "Шла четная неделя ледникового периода... Мы выживали как могли" \
            if (week_number % 2) == 0 else "Нечетная неделя"
        return {'message': week_parity}


def bot_python(msg):
    """/python"""
    if msg_command(msg) == '/python':
        if random.randint(0, 1) == 0:
            return {'message': 'Шшшшш...', 'attachment': 'photo348580470_401471407'}
        else:
            return {'message': 'Python - лучший язык'}


def bot_random(msg):
    """/random"""
    if msg_command(msg) == '/random':
        return {'message': random.random()}


def bot_zen(msg):
    """/дзен"""
    if msg_command(msg) == '/дзен':
        s = '''Ъарбштюх ыгзих, зхь гаюфыштюх.
Птэюх ыгзих, зхь эхптэюх.
Яаюбвюх ыгзих, зхь быюцэюх.
Быюцэюх ыгзих, зхь чрягврээюх.
Яыюбъюх ыгзих, зхь тыюцхээюх.
Арчахцхээюх ыгзих, зхь яыювэюх.
Зшврхьюбвм шьххв чэрзхэшх.
Юбюслх быгзрш эх эрбвюымъю юбюслх, звюсл эрагирвм яартшыр.
Яаш нвюь яаръвшзэюбвм трцэхх схчгяахзэюбвш.
Юишсъш эшъюуфр эх фюыцэл чрьрызштрвмбп.
Хбыш эх чрьрызштровбп птэю.
Тбвахвшт фтгбьлбыхээюбвм, ювсаюбм шбъгихэшх гурфрвм.
Фюыцхэ бгйхбвтютрвм юфшэ — ш, цхырвхымэю, вюымъю юфшэ — юзхтшфэлщ бяюбюс бфхырвм нвю.
Еювп юэ яюэрзрыг ьюцхв слвм ш эх юзхтшфхэ, хбыш тл эх уюыырэфхж.
Бхщзрб ыгзих, зхь эшъюуфр.
Еювп эшъюуфр чрзрбвго ыгзих, зхь яапью бхщзрб.
Хбыш ахрышчржшо быюцэю юскпбэшвм — шфхп яыюер.
Хбыш ахрышчржшо ыхуъю юскпбэшвм — шфхп, тючьюцэю, еюаюир.
Яаюбварэбвтр шьёэ — ювышзэрп ивгър! Сгфхь фхырвм ше яюсюымих!'''

        d = {}
        for c in (0x0410, 0x0430):
            for i in range(32):
                d[chr(i+c)] = chr((i+16) % 32 + c)

        return {'message': "".join([d.get(c, c) for c in s])}


def bot_matan(msg):
    """/матан"""
    if msg_command(msg) == '/матан':
        city = ['Югорск', 'Казахстан', 'Петербург', 'МСГ']
        photos = ['photo87425516_406709633', 'photo24524121_389966755', 'photo22195634_374008826']
        action = ['конину', 'кумыса', 'учиться', 'погулять', 'на посвят в восьмерку', 'на допсу по физике',
                  'на допсу по матану', 'научиться кодить', 'в общагу', 'сдать матан']
        action2 = ['стать богом', 'стать йогом', 'сбежать из дома', 'пойти на концерт Алисы', 'надеть колпак',
                   'выучить матан', 'поступить в ЛЭТИ', 'стать зав.кафедры ВМ']

        story = '''В небольшом селе {0} жил был маленький мальчик Андрюша.
Захотел как-то Андрюша {1}, но мамка не разрешила :C
И тогда решил Андрюшка {2} и {3}.
Больше его никто не видел.'''.format(random.choice(city), random.choice(action),
                                     random.choice(action2), random.choice(action2))

        return {'message': story, 'attachment': random.choice(photos)}


def bot_kappa(msg):
    emotes = vkapi.photos.get(album_id=228083099)['items']
    a = ''
    for emote in emotes:
        if re.compile(r'\b({0})\b'.format(emote['text'])).search(msg['body']) is not None:
            if a != '':
                a += ','
            a += 'photo348580470_' + str(emote['id'])
    if a != '':
        return {'message':str(random.random()),'attachment':a}

commands = [bot_help,
            bot_anec,
            bot_status,
            bot_random,
            bot_isin,
            bot_google,
            bot_schedule,
            bot_week,
            bot_python,
            bot_zen,
            bot_matan,
            bot_kappa]

# главный цикл
while True:
    try:
        longpoll = vkapi.messages.getLongPollServer(need_pts=1, use_ssl=0)
        ts = longpoll['ts']

        try:
            pts = newpts['new_pts']
        except NameError:
            pts = longpoll['pts']

        newpts = vkapi.messages.getLongPollHistory(pts=pts, ts=ts, fields='')

        for msg in newpts['messages']['items']:
            if msg['out'] == 0:
                if 'chat_id' in msg:
                    uid = 2000000000 + msg['chat_id']
                else:
                    uid = msg['user_id']

                # команды
                for cmd in commands:
                    reply = cmd(msg)  # Выполняется каждая команда, проверки на соответствие выполнены внутри них
                    if reply is not None:  # Команда возвращает либо kwargs для messages.send
                        if reply is not True:  # Либо True, если отправлять ответ не требуется
                            vkapi.messages.send(peer_id=uid, **reply)
                        break

        time.sleep(3)

    except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError, vk.exceptions.VkAPIError) as e:
        #        print('Fuck!')
        print(e)
        with open("bot.log",'a') as logfile:
            logfile.write(e.__class__.__name__ + str(e))
    except KeyboardInterrupt:
        raise
    except:
        with open("bot.log",'a') as logfile:
            logfile.write(e.__class__.__name__ + str(e))
