from bot import BotPlugin

test = BotPlugin()

@test.init
def init():
    print "hello"

@test.command('test')
def say_something(bot, user, channel, msg):
    with test.stored("abc", 0) as x:
        bot.msg(channel, x.data)
        x.data += 1
