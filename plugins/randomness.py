# -*- coding: utf-8 -*-
from bot import BotPlugin
import copy
import random
import os.path
import re

randomness = BotPlugin()


@randomness.command(['coin', 'flip'])
def coincmd(bot, user, channel, msg):
    bot.msg(channel, random.choice(('head', 'tail')))


@randomness.command([u'münze', 'muenze'])
def muenzecmd(bot, user, channel, msg):
    bot.msg(channel, random.choice(('Kopf', 'Zahl')))


@randomness.command('frage')
def magiccmd(bot, user, channel, msg):
    choices = [
        "Ja.",
        "Nein.",
        "ja, gewiss",
        "nein, niemals",
        "was faellt dir ein!",
        "Welch schaendlicher Gedanke!",
        "Das wuerde dem Meister gefallen",
        "Mitnichten wuerde ich das verneinen",
        ]
    bot.msg(channel, random.choice(choices))


@randomness.command(['magic', 'question', 'ask'])
def magiccmd2(bot, user, channel, msg):
    choices = [
        'As I see it, yes.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        "Don't count on it.",
        'It is certain.',
        'It is decidedly so.',
        'Most likely.',
        'My reply is no.',
        'My sources say no.',
        'No!',
        'Outlook good.',
        'Outlook not so good.',
        'Reply hazy, try again.',
        'Signs point to yes.',
        'Very doubtful.',
        'Without a doubt.',
        'Yes - definitely.',
        'Yes.',
        'You may rely on it.',
    ]
    bot.msg(channel, random.choice(choices))


@randomness.command('spin')
def spincmd(bot, user, channel, msg):

    def got_names(nicklist):
        # remove all @ in nicklist
        nicklist = [i.replace('@', '') for i in nicklist]
        if bot._get_nickname() in nicklist:
            nicklist.remove(bot._get_nickname())
        bot.msg(channel, "Die Flasche zeigt auf %s!" %
                random.choice(nicklist))

    bot.names(channel).addCallback(got_names)
