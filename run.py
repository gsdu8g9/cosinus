#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bot
from bot_config import config


vkbot = bot.VkBot(config)
vkbot.scheduler.start()
vkbot.listen()
