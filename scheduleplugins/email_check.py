import imaplib
import os
import vk
from bot import AbstractSchedulePlugin
from email.parser import Parser
from email.header import decode_header


class SchedulePlugin(AbstractSchedulePlugin):

    interval = {'seconds':60}


    def print_email_header(header_messages):
        res = ''

        for msg in header_messages:
            try:
                if (msg[1] != None):
                    res += (msg[0].decode(msg[1]) + ' ')
                else:
                    # не костыль, а костылище
                    res += (str(msg[0])[2:][:-1] +' ')

            except UnicodeEncodeError:
                #print('[Ошибка] Неизвестная кодировка!')
                pass

        res += '\n'

        return res


    def call(self):
        # смотрим время прошлой проверки
        if (os.path.isfile("last_check.dat") and (os.path.getsize("last_check.dat") > 0)):
            f = open("last_check.dat", "r")
            sdate = f.readline().split('\n')[0]
            last_check_date = datetime.datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S.%f')
            f.close()
        else:
            last_check_date = datetime.datetime.now()

        # обновляем дату проверки как текущую
        f = open("last_check.dat", "w")
        f.write(str(datetime.datetime.now()) + '\n')
        f.close()

        # логинимся
        imap = imaplib.IMAP4_SSL("imap.mail.ru")
        imap.login(EMAIL_LOGIN, EMAIL_PASSWORD)

        # заходим во входящие
        imap.select()

        # получаем входящие письма
        status, response = imap.search(None, 'ALL')
        all_msgs = response[0].split()

        n = 0

        response = ""

        for e_id in all_msgs:
            # оставляем только заголовок
            _, raw_email = imap.fetch(e_id, '(BODY[HEADER])')
            raw_email = raw_email[0][1].decode('utf-8')
            msg = Parser().parsestr(raw_email)

            # смотрим дату прихода сообщения
            str_date = decode_header(msg['Date'])[0][0]
            receive_date = datetime.datetime.utcfromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(str_date)))

            # если сообщение пришло позже, чем прошлая проверка, то запоминаем его
            if (receive_date > last_check_date):
                n += 1
                response += str(n) + ') '

                email_from = decode_header(msg['From'])
                response += print_email_header(email_from)

                email_subj = decode_header(msg['Subject'])
                response += 'Тема: ' + print_email_header(email_subj) + '\n'

        if n > 0:
            response = 'На почте ' + str(n) + ' новых сообщений:\n' + response
            response += "https://e.mail.ru/messages/inbox\n" 

            #print(response)
            self.bot.vkapi.messages.send(message=response, peer_id=2000000001, random_id=random.randint(1, 12345678))
            imap.close()
