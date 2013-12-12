from bot import BotPlugin
import requests
from lib.pluginloader import get_plugin

channel = BotPlugin()


@channel.command('join')
def join(bot, user, channel, msg):
    """join <channel> - Join a channel"""
    args = msg.split()
    if msg and len(args) > 0:
        print args
        for arg in args:
            print arg
            bot.join(str(arg))
            bot.msg(channel, 'Joined %s' % arg)


@channel.command('part')
def part(bot, user, channel, msg):
    """part <channel> - Leave a channel"""
    args = msg.split()
    if msg and len(args) > 0:
        for arg in args:
            bot.part(str(arg))
    else:
        bot.msg(channel, 'Bye')
        bot.part(str(channel))

