from bot import BotPlugin

yo = BotPlugin()


@yo.command('yo')
def show_yo(bot, user, channel, msg):
    """
        Send yo to someone
    """
    username = user.split('!')[0]
    m = "Yo!"
    bot.msg(username, m)
