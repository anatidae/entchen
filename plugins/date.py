from bot import BotPlugin

date = BotPlugin()

@date.startswith('!date')
def say_date(bot, user, channel, msg):
    m = "Date: %s" % time.strftime("%a, %b %d, %Y", time.localtime())
    bot.msg(channel, m)
