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
        for elem in sp:
            to_user = str(elem)
            bot.msg(to_user, m)
    except:
        bot.msg(channel, "!yo <nick>")


@yo.command('noe')
def show_noe(bot, user, channel, msg):
    """
        Send noe to someone
    """
    username = user.split('!')[0]
    m = "%s sends you: Noe!" % username
    sp = msg.split()
    try:
        for elem in sp:
            to_user = str(elem)
            bot.msg(to_user, m)
    except:
        bot.msg(channel, "!noe <nick>")
