import imaplib
import random

from bot import AbstractSchedulePlugin
import email
from email.header import decode_header
import email.utils
import time
import logging


def really_decode_header(encoded_header):
    return ''.join([decoded.decode(charset or 'utf-8')
                    for (decoded, charset)
                    in decode_header(encoded_header)])


class SchedulePlugin(AbstractSchedulePlugin):

    def __init__(self, bot):
        super(SchedulePlugin, self).__init__(bot)
        self.config = self.bot.config['email_check']
        self.interval = self.config["interval"]
        self.lastcheck = {x: time.time() for x in self.config["mailboxes"].keys()}

    def call(self):
        # 1: {
        #     "server": "imap.mail.ru",
        #     "credentials": ("login", "password")
        # }
        for (chat_id, server) in self.config["mailboxes"].items():
            logging.warning("Mailcheck %d %d" % (chat_id, self.lastcheck[chat_id]))
            try:
                imap = imaplib.IMAP4_SSL(server["server"])
                imap.login(*server['credentials'])
                # заходим во входящие
                imap.select()

                status_s, response_s = imap.search(None, 'ALL')
                checktime = time.time()

                if status_s != 'OK':
                    raise Exception("email_check on 'search all'")

                new_msgs = []

                for num in reversed(response_s[0].split()):
                    status_f, response_f = imap.fetch(num, '(BODY[HEADER])')

                    if status_f != 'OK':
                        raise Exception("email_check on 'fetch %s'" % num.decode())

                    header = email.message_from_bytes(response_f[0][1])
                    header_date = email.utils.mktime_tz(email.utils.parsedate_tz(header["Date"]))

                    if header_date < self.lastcheck[chat_id]:
                        break

                    header_from = really_decode_header(header["From"])

                    if header_from.find("<no-reply@accounts.google.com>") != -1:
                        continue

                    try:
                        header_subj = really_decode_header(header["Subject"])
                    except:
                        header_subj = "<Без темы>"

                    new_msgs.append((header_from, header_subj))

                if new_msgs:
                    response_v = []
                    response_v.append("На почте %d новых сообщений" % len(new_msgs))

                    for msg in new_msgs:
                        response_v.append("От: %s\nТема: %s" % msg)

                    response_v.append(server["page"])

                    self.bot.vkapi.messages.send(message='\n'.join(response_v), chat_id=chat_id, random_id=random.randint(1, 12345678))

                self.lastcheck[chat_id] = checktime

            except:
                logging.exception('email_check')
