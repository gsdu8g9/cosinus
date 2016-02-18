#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import importlib
import logging

import requests
import vk

import settings

start_time = datetime.datetime.now()

logger = logging.getLogger()
handler = logging.StreamHandler()
logger.addHandler(handler)
handler = logging.FileHandler("bot.log", "w", encoding="utf8")
logger.addHandler(handler)


def connect_long_poll_server(values):
    server = 'http://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=74'.format(**values)
    request = requests.request("GET", server, timeout=30)
    request.raise_for_status()
    return request.json()


if settings.auth_method == 'token':
    session = vk.Session(access_token=settings.token)
elif settings.auth_method == 'password':
    session = vk.AuthSession(app_id=settings.appid, user_login=settings.login,
                             user_password=settings.password, scope=settings.scope)
else:
    raise ValueError("Указан неверный auth_method")

vkapi = vk.API(session, v='5.45')
longpoll_server_info = vkapi.messages.getLongPollServer()

plugins_l = {
    -1: [],
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
    12: [],
    13: [],
    14: [],
    15: [],
    51: [],
    61: [],
    62: [],
    70: [],
    80: [],
    114: []
}

if __name__ == '__main__':
    for plugin_name in settings.plugins:
        plug = importlib.import_module('plugins.' + plugin_name)
        plugins_l[plug.event_id] += [plug.call]

    while True:
        try:
            updates = connect_long_poll_server(longpoll_server_info)
        except requests.exceptions.ReadTimeout:
            pass
        else:
            if 'failed' not in updates:
                longpoll_server_info['ts'] = updates['ts']
                for update in updates['updates']:
                    for plugin in plugins_l[update[0]] + plugins_l[-1]:
                        try:
                            plugin(update)
                        except vk.exceptions.VkAPIError as e:
                            logging.exception('')
                            pass
            elif updates['failed'] in (2, 3):
                longpoll_server_info = vkapi.messages.getLongPollServer()
            elif updates['failed'] == 1:
                longpoll_server_info['ts'] = updates['ts']
