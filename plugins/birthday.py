from bot import BotPlugin

sysinfo = BotPlugin()

@sysinfo.command('birthday')
def birthday(bot, user, channel, msg):
    bot.msg(channel, 'kindchen singt mit allen im Chor: '
            '"Happy Birthday dear %s, Happy Birthday to you!"' % msg)
