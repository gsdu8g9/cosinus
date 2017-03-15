#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
# import json
# from collections import OrderedDict
from threading import Thread
import requests
from apscheduler.schedulers.background import BackgroundScheduler

import vk_api
import longpoll


class VkBot(object):
    def __init__(self, config):
        self.config = config
        self._vksession = vk_api.VkApi(
            login=self.config['bot']['login'],
            password=self.config['bot']['password'],
            number=self.config['bot'].get('number'))
        self._vksession.authorization()
        self.api = self._vksession.get_api()
        self.bot_id = self.api.users.get()[0]['id']
        self.longpoll = longpoll.VkLongPoll(self._vksession)
        self.plugins = dict()
        self._lp_parsers = dict()
        self.scheduler = BackgroundScheduler()

        for plugin_name in set(self.config["bot"]["plugins"]):
            plugin = importlib.import_module("plugins." + plugin_name)
            self.plugins[plugin_name] = plugin.Plugin(self)

    # def loadconf(self):
    #     with open(self._configfile, "r", encoding="utf-8") as f:
    #         self.config = json.load(f, object_pairs_hook=OrderedDict)

    # def saveconf(self):
    #     with open(self._configfile, "w", encoding="utf-8") as f:
    #         json.dump(self.config, f, ensure_ascii=False, indent=4)

    def upload_message_photo(self, photos):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        files = {("file%d" % n): (("file%d.png" % n), f, "image/png") for n, f in enumerate(photos)}
        send_response = requests.post(upload_url, files=files)
        save_response = self.api.photos.saveMessagesPhoto(**send_response.json())
        return save_response

    def upload_audio(self, audio):
        upload_url = self.api.audio.getUploadServer()['upload_url']
        files = {'file': ("file.mp3", audio, "audio/mpeg")}
        send_response = requests.post(upload_url, files=files)
        save_response = self.api.audio.save(**send_response.json())
        return save_response

    def add_longpoll_parser(self, name, function):
        if name in self._lp_parsers:
            raise KeyError
        self._lp_parsers[name] = function

    def listen(self):
        for event in self.longpoll.listen():
            for lp_parser in self._lp_parsers.values():
                parse_thread = Thread(target=lp_parser, args=[event])
                parse_thread.start()
