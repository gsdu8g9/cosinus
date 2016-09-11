#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import time
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


class vkApiThrottle(vk.API):
    _lastcall = time.time()

    def __getattr__(self, method_name):
        while (time.time() - self._lastcall < settings.vk_throttle):
            time.sleep(settings.vk_throttle)
        self._lastcall = time.time()
        return vk.api.Request(self, method_name)

class VkUpdates(object):
    def __init__(self, vkapi):
        self.updates = []
        self.vkapi = vkapi
        self.server_values = self.vkapi.messages.getLongPollServer()
        self.server_values['wait'] = 25
        self.server_values['mode'] = 0b11101010
        self.server_values['version'] = 1

    def server_url(self):
        return 'https://{server}?act=a_check&key={key}&ts={ts}' \
               '&wait={wait}&version={version}'.format(**self.server_values)

    def _get(self):
        request = requests.request("GET", self.server_url(), timeout=30)
        request.raise_for_status()
        return request.json()

    def _update(self):
        response = self._get()
        if 'failed' in response:
            if response['failed'] == 1:
                self.server_values['ts'] == response['ts']
            elif response['failed'] == 2:
                new_values = self.vkapi.messages.getLongPollServer()
                self.server_values['key'] = new_values['key']
            elif response['failed'] == 3:
                new_values = self.vkapi.messages.getLongPollServer()
                self.server_values['key'] = new_values['key']
                self.server_values['ts'] = new_values['ts']
            elif response['failed'] == 4:
                raise ValueError
        else:
            self.server_values['ts'] = response['ts']
            self.updates += response["updates"]

    def pop(self):
        while not self.updates:
            self._update()
        return self.updates.pop(0)


session = vk.Session(access_token=settings.token)
vkapi = vkApiThrottle(session, v='5.52')
bot_id = vkapi.users.get()[0]['id']
plugins_list = []


if __name__ == '__main__':
    for plugin_name in settings.plugins:
        plug = importlib.import_module('plugins.' + plugin_name)
        plugins_list += [plug.call]

    queue = VkUpdates(vkapi)

    while True:
        try:
            update = queue.pop()
            for plugin in plugins_list:
                try:
                    plugin(update)
                except vk.exceptions.VkAPIError:
                    logging.exception('')
        except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError):
            pass
        except KeyboardInterrupt:
            raise
        except:
            logging.exception('')
