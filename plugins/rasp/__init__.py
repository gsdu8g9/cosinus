import datetime
import json
import os

from bot import vkapi

event_id = 4
time_offset = datetime.timedelta(hours=8)

rasp = json.load(open(os.path.join(os.path.dirname(__file__), 'rasp.json'), encoding='utf8'))


def call(event):
    if event[6].partition(' ')[0] == '/пары':
        current_time = datetime.datetime.now() + time_offset

        week_number = current_time.isocalendar()[1] % 2
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

        for lesson in rasp[current_time.weekday()]:
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

        vkapi.messages.send(message='\n'.join(reply), peer_id=event[3])
