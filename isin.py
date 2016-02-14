#!/usr/bin/env python
import datetime
import json
import os
import sqlite3
import sys
import time

import vk

isin = 328822798

try:
    dbpath = os.environ['OPENSHIFT_DATA_DIR'] + 'isin.sqlite'
except KeyError:
    dbpath = './isin.sqlite'

vkapi = vk.API(vk.Session(), v=5.45)


def getphoto():
    db = sqlite3.connect(dbpath)
    dbcursor = db.cursor()
    users_req = vkapi.users.get(user_ids=isin, fields='photo_id')
    if 'photo_id' in users_req[0]:
        photo_id = users_req[0]['photo_id']
        photo_req = vkapi.photos.getById(photos=photo_id)
        photo_w = photo_req[0]['width']
        if 'photo_' + str(photo_w) in photo_req[0]:
            photo_url = photo_req[0]['photo_' + str(photo_w)]
        elif 'photo_2560' in photo_req[0]:
            photo_url = photo_req[0]['photo_2560']
        elif 'photo_1280' in photo_req[0]:
            photo_url = photo_req[0]['photo_1280']
        elif 'photo_807' in photo_req[0]:
            photo_url = photo_req[0]['photo_807']
        elif 'photo_604' in photo_req[0]:
            photo_url = photo_req[0]['photo_604']
        elif 'photo_130' in photo_req[0]:
            photo_url = photo_req[0]['photo_130']
        elif 'photo_75' in photo_req[0]:
            photo_url = photo_req[0]['photo_75']

        dbcursor.execute('INSERT OR REPLACE INTO photo VALUES (?);', (photo_url,))
        db.commit()
        db.close()


def readphoto():
    db = sqlite3.connect(dbpath)
    dbcursor = db.cursor()
    photos_url = []
    photos = dbcursor.execute('SELECT * FROM photo;')
    for row in photos:
        photos_url += [row[0]]
    db.close()
    return '\n'.join(photos_url)


def getwall():
    db = sqlite3.connect(dbpath)
    dbcursor = db.cursor()
    wall = vkapi.wall.get(owner_id=isin, count=100)
    for item in wall['items']:
        dbcursor.execute('INSERT OR REPLACE INTO wall VALUES (?,?);',
                         (item['id'], json.dumps(item, ensure_ascii=False)))
    db.commit()
    db.close()


def readwall():
    db = sqlite3.connect(dbpath)
    dbcursor = db.cursor()
    items = []
    count = 0
    wall = dbcursor.execute('SELECT * FROM wall;')
    for row in wall:
        count += 1
        content = json.loads(row[1])
        items.append(content)
    db.close()
    resp = {'count': count, 'items': items}
    resp = {'response': resp}
    return json.dumps(resp, ensure_ascii=False, indent=4)


def getstatus():
    db = sqlite3.connect(dbpath)
    dbcursor = db.cursor()
    info = vkapi.users.get(user_ids=isin, fields='online')
    if info[0]['online'] == 1:
        online_mobile = 1 if 'online_mobile' in info else 0
        dbcursor.execute('INSERT OR REPLACE INTO status VALUES (?,?);', (str(int(time.time())), str(online_mobile)))
    else:
        dbcursor.execute('DELETE FROM status WHERE time = (?);', (str(int(time.time())),))
    db.commit()
    db.close()


def readstatus(date=None):
    db = sqlite3.connect(dbpath)
    dbcursor = db.cursor()
    statuses = []
    if date is not None:
        request = dbcursor.execute(
                '''SELECT STRFTIME('%H:%M %d-%m-%Y',time+60*60*3,'unixepoch'),mobile FROM status
                   WHERE STRFTIME('%d%m%Y',time+60*60*3,'unixepoch')=(?);''',
                (date,))
    else:
        request = dbcursor.execute('''SELECT STRFTIME('%H:%M %d-%m-%Y',time+60*60*3,'unixepoch'),mobile FROM status;''')
    for row in request:
        statuses += [row[0] + (' mobile' if row[1] == '1' else '')]
    db.close()
    return '\n'.join(statuses)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'status':
            getstatus()
    except IndexError:
        getwall()
        getphoto()

    # getaudio()
    print('Success')
