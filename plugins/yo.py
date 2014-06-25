from bot import BotPlugin

yo = BotPlugin()


@yo.command('yo')
def show_yo(bot, user, channel, msg):
    """
        Send yo to someone
    """
    username = user.split('!')[0]
    m = "%s sends you: Yo!" % username
    sp = msg.split()
    try:
        to_user = str(sp[0])
        bot.msg(to_user, m)
    except:
        bot.msg(channel, "!yo <nick>")
