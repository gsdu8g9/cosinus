import datetime

from bot import AbstractChatPlugin
from .rasp_a import rasp_a, rasp_t
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

def format_lesson(lesson):

    return ("Предмет: {name}\n"
            "Начало: {start}\n"
            "Окончание: {end}\n"
            "Аудитория: {aud}\n"
            "Препод: {teacher}").format(name=lesson['name'], 
                                        start=rasp_t[lesson['time']]['start'].strftime('%H:%M'),
                                        end=rasp_t[lesson['time']]['end'].strftime('%H:%M'),
                                        aud=lesson['class'],
                                        teacher=lesson['teacher'])


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
            group = self.bot.config['rasp'][str(self.members[event[3]])]
            current_time = datetime.datetime.now(tz=msk)
            week_parity = 2 if current_time.isocalendar()[1] % 2 == 0 else 1

            current_lesson = None
            next_lesson = None

            try:
                today_rasp = rasp_fix[group][current_time.date()]
            except KeyError:
                today_rasp = rasp_a[group][current_time.weekday()]


            for lesson in today_rasp:
                if lesson['week'] == 0 or lesson['week'] == week_parity:
                    if (current_time.time() > rasp_t[lesson['time']]['start']) and \
                       (current_time.time() < rasp_t[lesson['time']]['end']):
                        current_lesson = lesson
                    if current_time.time() < rasp_t[lesson['time']]['start']:
                        next_lesson = lesson
                        break
            else:
                # Мало того, что оно работает, так я ещё и не представляю, как это сделать красивым
                i = 1
                next_lesson = None
                while not next_lesson:
                    try:
                        next_day_rasp = rasp_fix[group][current_time.date() + datetime.timedelta(days=i)]
                    except KeyError:
                        next_day_rasp = rasp_a[group][(current_time.weekday() + i) % 7]
                        if (current_time.weekday() + i) == 7:
                            week_parity = 1 if week_parity == 2 else 2
                    i += 1
                    try:
                        j = 0
                        while next_day_rasp[j]['week'] not in (0, week_parity):
                            j += 1
                        next_lesson = next_day_rasp[j]
                    except IndexError:
                        pass

            reply = []

            if current_lesson is not None:
                reply += ['Текущая пара:']
                reply += [format_lesson(current_lesson)]
            else:
                reply += ['Сейчас пары нет']

            if next_lesson is not None:
                reply += ['Следующая пара:']
                reply += [format_lesson(next_lesson)]

            self.bot.vkapi.messages.send(message='\n'.join(reply), peer_id=event[3])
