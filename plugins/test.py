# -*- coding: utf-8 -*-
from bot import BotPlugin

test = BotPlugin()


@test.init
def init(bot):
    print "init"
    test.stored.setdefault("abc", 0)


@test.command('test')
def say_something(bot, user, channel, msg):
    print "test"
    with test.stored("abc") as x:
        bot.msg(channel, x.data)
        x.data += 1

# @test.periodic(1)
# def x():
#     print "a"
