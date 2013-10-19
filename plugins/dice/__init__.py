from bot import BotPlugin
from dice import roll
import random


dice = BotPlugin()


@dice.init
def init():
    random.seed()


@dice.command(['roll', 'dice', 'wuerfel'])
def do_roll(bot, user, channel, msg):
    bot.msg(channel, roll(msg))
