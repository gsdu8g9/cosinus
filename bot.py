#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import time
import importlib
import configparser
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

import requests
import vk
import logging


class vkApiThrottle(vk.API):
    _lastcall = time.time()

    def __getattr__(self, method_name):
        while (time.time() - self._lastcall < 0.34):
            time.sleep(0.34)
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
                self.server_values['ts'] = response['ts']
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
            try:
                self._update()
            except (requests.exceptions.ReadTimeout, requests.exceptions.HTTPError):
                pass
        return self.updates.pop(0)


class VkBot(object):
    def __init__(self, configfile):
        self.configfile = configfile
        self.config = configparser.ConfigParser()
        self.config.read(self.configfile)

        self.admins = [int(x) for x in self.config['general']['admins'].split(',')]

        self.session = vk.Session(access_token=self.config['general']['token'])
        self.vkapi = vkApiThrottle(self.session, v='5.57')
        self.bot_id = self.vkapi.users.get()[0]['id']
        self.scheduler = BackgroundScheduler()

        self.chat_queue = VkUpdates(self.vkapi)

        self.chatplugins = {}
        self.scheduleplugins = {}

        for plugin_name in self.config['general']['chatplugins'].split(','):
            plugin = importlib.import_module('chatplugins.' + plugin_name)
            self.chatplugins[plugin_name] = plugin.ChatPlugin(self)

        for plugin_name in self.config['general']['scheduleplugins'].split(','):
            plugin = importlib.import_module('scheduleplugins.' + plugin_name)
            self.scheduleplugins[plugin_name] = plugin.SchedulePlugin(self)

        for plugin_name, plugin in self.scheduleplugins.items():
            self.scheduler.add_job(plugin.call, id=plugin_name, trigger='interval', **plugin.interval)


    def parse_chat(self):
        update = self.chat_queue.pop()
        for plugin_name, plugin in self.chatplugins.items():
            thread = Thread(target=plugin.call, args=[update])
            thread.start()

    def parse_chat_forever(self):
        while True:
            try:
                self.parse_chat()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logging.exception('')


class AbstractPlugin(object):
    def __init__(self, bot):
        self.bot = bot

class AbstractChatPlugin(AbstractPlugin):
    def call(self, event):
        return

class AbstractSchedulePlugin(AbstractPlugin):
    interval = {'seconds':59, 'weeks':4}

    def __init__(self, bot):
        super(AbstractSchedulePlugin, self).__init__(bot)
        self.interval = {'seconds':59, 'weeks':4}

    def call(self):
        return


def main():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    handler = logging.FileHandler("bot.log", "w", encoding="utf8")
    logger.addHandler(handler)
    vkbot = VkBot('config.ini')
    vkbot.scheduler.start()
    vkbot.parse_chat_forever()


if __name__ == '__main__':
    main()