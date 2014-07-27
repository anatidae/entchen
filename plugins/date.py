# coding=utf-8

from bot import BotPlugin
import time

date = BotPlugin()


@date.command('date')
def say_date(bot, user, channel, msg):
    """ show current date
    """
    m = "%s" % time.strftime("%a, %b %d, %Y", time.localtime())
    bot.msg(channel, m)


@date.command('time')
def say_time(bot, user, channel, msg):
    """ show current time
    """
    m = "%s" % time.strftime("%I:%M %p", time.localtime())
    bot.msg(channel, m)


@date.command('dt')
def say_datetime(bot, user, channel, msg):
    """Print current date and time"""
    m = "Today is %s and it's %s" % (
        time.strftime("%a, %b %d, %Y", time.localtime()),
        time.strftime("%I:%M %p", time.localtime())
    )
    bot.msg(channel, m)
