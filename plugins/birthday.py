from bot import BotPlugin

birthday = BotPlugin()


@birthday.command('birthday')
def birthdaycmd(bot, user, channel, msg):
    bot.msg(channel, 'kindchen singt mit allen im Chor: '
            '"Happy Birthday dear %s, Happy Birthday to you!"' % msg)
