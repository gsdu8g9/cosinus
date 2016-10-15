import datetime

from bot import AbstractChatPlugin
from .rasp_a import rasp_a, rasp_t
from .rasp_fix import rasp_fix


class MskTime(datetime.tzinfo):
    def tzname(self, dt):
        return "Europe/Moscow"
    def dst(self, dt):
        return datetime.timedelta(0)
    def utcoffset(self, dt):
        return datetime.timedelta(hours=3)


msk = MskTime()


def format_lesson(lesson, time):
    return ("Предмет: {name}\n"
            "Начало: {start}\n"
            "Окончание: {end}\n"
            "Аудитория: {aud}\n"
            "Препод: {teacher}").format(name=lesson['name'],
                                        start=rasp_t[time]['start'].strftime('%H:%M'),
                                        end=rasp_t[time]['end'].strftime('%H:%M'),
                                        aud=lesson['class'],
                                        teacher=lesson['teacher'])


class ChatPlugin(AbstractChatPlugin):

    def __init__(self, bot):
        super(ChatPlugin, self).__init__(bot)
        self.chats = self.bot.config['rasp'].keys()
        self.members = {}
        chatinfo = self.bot.vkapi.messages.getChat(chat_ids=",".join(map(lambda x: str(x), self.chats)))
        for chat in chatinfo:
            for user_id in chat['users']:
                if user_id != self.bot.bot_id:
                    self.members[user_id] = chat['id']

    def call(self, event):
        if event[0] == 4 and event[6].partition(' ')[0].lower() == '/пары':
            if (event[3] - 2000000000) in self.chats:
                group = self.bot.config['rasp'][event[3]]
            elif event[3] in self.members.keys():
                group = self.bot.config['rasp'][self.members[event[3]]]
            else:
                return

            l_pydate = datetime.datetime.now(tz=msk).date()
            now_pytime = datetime.datetime.now(tz=msk).time()

            now = False
            if now_pytime < rasp_t[1]['start']:
                l_pydate -= datetime.timedelta(days=1)
                l_time = 5
            else:
                l_time = -1
                for v in rasp_t:
                    if now_pytime < v['start']:
                        break
                    elif v['start'] <= now_pytime <= v['end']:
                        l_time += 1
                        now = True
                        break
                    l_time += 1
            l_weekday = l_pydate.weekday()
            l_parity = 1 if l_pydate.isocalendar()[1] % 2 else 2

            reply = []

            if not now:
                current_lesson = None
            else:
                try:
                    today_rasp = rasp_fix[group][l_pydate]
                except KeyError:
                    today_rasp = rasp_a[group][l_weekday]
                try:
                    current_lesson = today_rasp[l_time, 0]
                except KeyError:
                    try:
                        current_lesson = today_rasp[l_time, l_parity]
                    except KeyError:
                        current_lesson = None

            if current_lesson:
                reply += ['Текущая пара:']
                reply += [format_lesson(current_lesson, l_time)]
            else:
                reply += ['Сейчас пары нет']


            next_lesson = None
            while not next_lesson:
                if l_time == 5:
                    if l_weekday == 6:
                        l_parity = 2 if l_parity == 1 else 1
                    l_pydate += datetime.timedelta(days=1)
                    l_weekday = (l_weekday+1) % 7
                l_time = (l_time+1) % 6
                try:
                    today_rasp = rasp_fix[group][l_pydate]
                except KeyError:
                    today_rasp = rasp_a[group][l_weekday]
                try:
                    next_lesson = today_rasp[l_time, 0]
                except KeyError:
                    try:
                        next_lesson = today_rasp[l_time, l_parity]
                    except KeyError:
                        next_lesson = None

            reply += ['Следующая пара:']
            reply += [format_lesson(next_lesson, l_time)]

            self.bot.vkapi.messages.send(message='\n'.join(reply), peer_id=event[3])
