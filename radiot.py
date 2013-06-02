#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmpp, time, sys, random
import datetime, re, urllib2

from text import is_txt

assert len(sys.argv[1:]) == 3, 'params required: <login> <password> <name>'

def return_podcast():
    req = urllib2.urlopen('http://www.radio-t.com')
    num = max(map(lambda x: int(x), re.findall('/podcast-([0-9]+)/', req.read()))) + 1
    req.close()
    num_to_smile = [':zero:',':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:']
    num_smile = ''.join(map(lambda x: num_to_smile[x], [int(i) for i in str(num)]))
    if all([datetime.datetime.utcnow().weekday() == 5, 19 <= datetime.datetime.utcnow().time().hour <= 23]):
        return '%s Сейчас наверно идет %s выпуск. Для уверенности можно подсмотреть здесь: http://www.radio-t.com' % (num_smile, num)
    return '%s В ожидании %s выпуска. Детали здесь: http://www.radio-t.com' % (num_smile, num)

is_txt['выпуск!'.decode('UTF-8')] = return_podcast()

is_txt['help!'] = "commands - " + ", ".join(is_txt.keys())

def send(conn, mess):
    try:
        mess = mess.decode('UTF-8')
    except:
        pass
    mymess = xmpp.protocol.Message(body=mess)
    mymess.setTo('online@conference.radio-t.com')
    mymess.setType('groupchat')
    conn.send(mymess)

def message_handler(conn, mess):
    try:
        text = mess.getBody()
        if text in is_txt and is_txt[text]:
            txt = is_txt[text]
            if type(txt) == list:
                txt = random.choice(txt)
            time.sleep(0.9)
            send(conn, txt)
    except:
        pass

cl = xmpp.Client('yandex.ru', debug=[])
cl.connect(server=('xmpp.ya.ru',5223))

cl.RegisterHandler('message', message_handler)

cl.auth(sys.argv[1], sys.argv[2], 'Python-JCB')

p = xmpp.Presence(to='online@conference.radio-t.com/%s' % sys.argv[3])
p.setTag('x',namespace=xmpp.NS_MUC).setTagData('password','')
p.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})

cl.send(p)
cl.sendInitPresence()

while True:
    try:
        cl.Process(1)
    except:
        cl.disconnect()
        cl.send(xmpp.Presence(typ = 'unavailable'))
        exit()

