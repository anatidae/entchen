# -*- coding: utf-8 -*-
from bot import BotPlugin
import copy
import random
import os.path

randomness = BotPlugin()

@randomness.command(['coin', 'flip'])
def coincmd(bot, user, channel, msg):
    bot.msg(channel, random.choice(('head', 'tail')))

@randomness.command(u'münze')
def muenzecmd(bot, user, channel, msg):
    bot.msg(channel, random.choice(('Kopf', 'Zahl')))

@randomness.command(['dice', 'w6'])
def dicecmd(bot, user, channel, msg):
    bot.msg(channel, str(random.choice((range(1,7)))))
