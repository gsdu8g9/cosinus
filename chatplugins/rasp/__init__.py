import datetime

from bot import AbstractChatPlugin
from .rasp_a import rasp_a
from .rasp_fix import rasp_fix

event_id = 4

class MskTime(datetime.tzinfo):
    def tzname(self, dt):
        return "Europe/Moscow"
    def dst(self, dt):
        return datetime.timedelta(0)
    def utcoffset(self, dt):
        return datetime.timedelta(hours=3)

msk = MskTime()


class ChatPlugin(AbstractChatPlugin):
    # help = """/пары - получить текущее и следующее занятие в расписании группы 5383 ЛЭТИ"""

    def __init__(self, bot):
        super(ChatPlugin, self).__init__(bot)
        self.chats = [int(x)+2000000000 for x in self.bot.config['rasp'].keys()]
        self.members = {}
        chatinfo = self.bot.vkapi.messages.getChat(chat_ids=",".join(self.bot.config['rasp'].keys()))
        for chat in chatinfo:
            for user_id in chat['users']:
              if user_id != self.bot.bot_id:
                self.members[user_id] = chat['id']



    def call(self, event):
        if event[0] == 4 and event[6].partition(' ')[0].lower() == '/пары' \
           and (event[3] in self.chats or event[3] in self.members.keys()):
            # TODO: имена переменных
            group = self.bot.config['rasp'][self.members[event[3]]]
            current_time = datetime.datetime.now(tz=msk)
            week_number = current_time.isocalendar()[1] % 2
            week_parity = 2 if week_number == 0 else 1

            current_lesson = None
            next_lesson = None

            # def get_lesson_time(st):
            #     t = datetime.datetime.strptime(st, '%H:%M')
            #     t = t.replace(year=current_time.year, month=current_time.month, day=current_time.day)
            #     return t

            def format_lesson(lesson):
                lesson_info = ['Предмет: ', lesson['name'], '\n',
                               'Начало: ', lesson['start'].strftime('%H:%M'), '\n',
                               'Окончание: ', lesson['end'].strftime('%H:%M'), '\n',
                               'Аудитория: ', lesson['class'], '\n',
                               'Препод: ', lesson['teacher']]
                return ''.join(lesson_info)

            try:
                today_rasp = rasp_fix[group][current_time.date()]
            except KeyError:
                today_rasp = rasp_a[group][current_time.weekday()]

            for lesson in today_rasp:
                if lesson['week'] == 0 or lesson['week'] == week_parity:
                    start = lesson['start']
                    end = lesson['end']
                    if (current_time.time() > start) and (current_time.time() < end):
                        current_lesson = lesson
                    if current_time.time() < start:
                        next_lesson = lesson
                        break
            else:
                i = 1
                while True:
                    try:
                        next_day_rasp = rasp_fix[group][current_time.date() + datetime.timedelta(days=i)]
                    except KeyError:
                        next_day_rasp = rasp_a[group][(current_time.weekday() + i) % 7]
                        if (current_time.weekday() + i) == 7:
                            week_parity = 1 if week_number == 2 else 2
                    i += 1
                    try:
                        while next_day_rasp[0]['week'] not in (0, week_parity):
                            next_day_rasp.pop(0)
                    except IndexError:
                        pass
                    if next_day_rasp:
                        break
                next_lesson = next_day_rasp[0]

            reply = []

            if current_lesson is not None:
                reply += ['Текущая пара:']
                reply += [format_lesson(current_lesson)]
            else:
                reply += ['Сейчас пары нет']

            if next_lesson is not None:
                reply += ['Следующая пара:']
                reply += [format_lesson(next_lesson)]
            else:
                reply += ['Что-то не так. Этот не должен быть достижим']

            self.bot.vkapi.messages.send(message='\n'.join(reply), peer_id=event[3])
