from bot import BotPlugin
import copy
import random
import os.path

chatter = BotPlugin()

@chatter.any
def say_voicing(bot, user, channel, msg):
    if bot.nickname in msg and not msg.startswith(bot.nickname):
        l = ["quak","quak","schnatter","quak quak"]
        bot.msg(channel, random.choice(l))

def get_data_from_file(fn=None):
    """ Read data from file.

    Syntax:
    <key>=<value>
    """
    d = {}
    if not fn:
        fn = os.path.join(os.path.dirname(__file__),
                          'chatter.data')
    
    fp = open(fn)
    for line in fp.readlines():
        x = line.split('=')
        if len(x)>1:
            d[x[0]] = x[1].strip()
    fp.close()
    return d

@chatter.any
def say_stuff(bot, user, channel, msg):
    messages = get_data_from_file()

    for m in messages.keys():
        if m in msg.lower():
            bot.msg(channel, messages.get(m))
