import imaplib
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
        # логинимся
        imap = imaplib.IMAP4_SSL("imap.mail.ru")
        imap.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        # заходим во входящие
        imap.select()

        # ищем только непросмотренные письма
        status, response = imap.search(None, 'UNSEEN')
        unread_msgs = response[0].split()

        n = len(unread_msgs)

        if n > 0:
            response = 'На почте' + str(n) + 'новых сообщений\n'

            for e_id in unread_msgs:
                # оставляем только заголовок
                _, raw_email = imap.fetch(e_id, '(BODY[HEADER])')
                raw_email = raw_email[0][1].decode('utf-8')
                msg = Parser().parsestr(raw_email)

                email_from = decode_header(msg['From'])
                response += ('От: ' + print_email_header(email_from))

                email_subj = decode_header(msg['Subject'])
                response += ('Тема: ' + print_email_header(email_subj))

            response += "\nhttps://e.mail.ru/messages/inbox\n" 

            self.bot.vkapi.messages.send(message=response, peer_id=96106441, random_id=random.randint(1, 12345678))

        imap.close()