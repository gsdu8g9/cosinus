#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import requests
import vk

import settings


def connect_long_poll_server(values):
    server = 'http://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2'.format(**values)
    request = requests.request("GET",server,timeout=30)
    return request.json()

def main():
    if settings.auth_method == 'token':
        session = vk.Session(access_token=settings.token)
    elif settings.auth_method == 'password':
        session = vk.AuthSession(app_id=settings.appid,user_login=settings.login,user_password=settings.password,scope=settings.scope)
    else:
        raise Exception('Неправильные настройки')

    vkapi = vk.API(session, v='5.45')

    plugins={}

    sys.path.insert(0,'plugins/')
    for plugin in settings.plugins:
        module = __import__(plugin)
        plugin = module.Plugin(vkapi)
        try:
            plugins[plugin.event_id] += [plugin]
        except KeyError:
            plugins[plugin.event_id] = [plugin]
    sys.path.pop(0)

    try:
        longpoll = vkapi.messages.getLongPollServer()
    except (requests.HTTPError, requests.Timeout) as e:
        print(e)
    else:
        while True:
            updates = connect_long_poll_server(longpoll)
            if 'failed' not in updates:
                for update in updates['updates']:
                    for plugin in plugins[update[0]]:
                        if plugin(update):
                            break
            elif updates['failed'] in (2,3):
                longpoll = vkapi.messages.getLongPollServer()
            elif updates['failed'] == 1:
                longpoll['ts'] = updates['ts']

if __name__ == '__main__':
    main()
