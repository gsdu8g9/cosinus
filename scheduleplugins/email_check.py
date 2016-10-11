import imaplib
import vk
import random
from bot import AbstractSchedulePlugin
from email.parser import Parser
from email.header import decode_header
import email.utils
import time

mailparser = Parser()


def really_decode_header(encoded_header):
    if type(encoded_header) is not str:
        raise TypeError("expected str as encoded_header")

    decoded_parts = []
    for (decoded, charset) in decode_header(encoded_header):
        if charset is None:
            if type(decoded) is str:
                decoded_parts.append(decoded)
            elif type(decoded) is bytes:
                decoded_parts.append(decoded.decode())
        else:
            decoded_parts.append(decoded.decode(charset))

    return ''.join(decoded_parts)


class SchedulePlugin(AbstractSchedulePlugin):

    def __init__(self, bot):
        super(SchedulePlugin, self).__init__(bot)
        self.interval = {'minutes': self.bot.config['email_check'].getint('interval')}
        self.lastcheck = time.time()

    def call(self):

        # логинимся
        imap = imaplib.IMAP4_SSL("imap.mail.ru")
        imap.login(self.bot.config['email_check']['user'], self.bot.config['email_check']['password'])
        # заходим во входящие
        imap.select()

        status_s, response_s = imap.search(None, 'ALL')

        if status_s != 'OK':
            raise Exception("email_check on 'search all'")

        new_msgs = []



        for num in reversed(response_s[0].split()):
            status_f, response_f = imap.fetch(num, '(BODY[HEADER])') 
            
            if status_f != 'OK':
                raise Exception("email_check on 'fetch %s'" % num.decode())

            raw_header = response_f[0][1].decode()
            header = mailparser.parsestr(raw_header)
            header_date = email.utils.mktime_tz(email.utils.parsedate_tz(header["Date"]))

            if header_date < self.lastcheck:
                break

            header_from = really_decode_header(header["From"])
            header_subj = really_decode_header(header["Subject"])

            new_msgs.append((header_from, header_subj))

        if new_msgs:
            response_v = []
            response_v.append("На почте %d новых сообщений" % len(new_msgs))

            for msg in new_msgs:
                response_v.append("От: %s\nТема: %s" % msg)

            response_v.append("https://e.mail.ru/messages/inbox")

            self.bot.vkapi.messages.send(message='\n'.join(response_v), peer_id=2000000001, random_id=random.randint(1, 12345678))

        self.lastcheck = time.time()
        imap.close()
