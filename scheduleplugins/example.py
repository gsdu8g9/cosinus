import vk
import random

from bot import AbstractSchedulePlugin

event_id = 4


class SchedulePlugin(AbstractSchedulePlugin):
    interval = {'seconds':20}

    def call(self):
        self.bot.vkapi.messages.send(message="Testing schedule", peer_id=96106441, random_id=random.randint(1, 12345678))
