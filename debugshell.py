import os
os.environ['PYTHONINSPECT'] = '1'

import vk
import settings

session = vk.Session(access_token=settings.token)
vkapi = vk.API(session, v='5.52')
