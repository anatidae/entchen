# -*- coding: utf-8 -*-
from bot import BotPlugin

yo = BotPlugin()


def send_message(bot, user, channel, msg, message):
    username = user.split('!')[0]
    m = "%s sends you: %s" % (username, message)
    sp = msg.split()
    try:
        for elem in sp:
            to_user = str(elem)
            bot.msg(to_user, m)
    except:
        return False


@yo.command('yo')
def show_yo(bot, user, channel, msg):
    """
        Send yo to someone
    """
    if send_message(bot, user, channel, msg, "Yo!"):
        bot.msg(channel, "!yo <nick>")


@yo.command('noe')
def show_noe(bot, user, channel, msg):
    """
        Send noe to someone
    """
    if send_message(bot, user, channel, msg, "Noe!"):
        bot.msg(channel, "!noe <nick>")
