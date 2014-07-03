from bot import BotPlugin
from twisted.internet import defer

userinfo = BotPlugin()


@userinfo.command("whoami")
def whoami(bot, user, channel, message):
    nickname, hostmask = user.split('!', 1)

    def say_result(result):
        if result:
            bot.msg(channel, "%s is logged in as %s" % (nickname, result))
        else:
            bot.msg(channel, "%s is not logged in" % (nickname))
    if nickname not in bot._whoiscallbacks:
        bot._whoiscallbacks[nickname] = defer.Deferred()
    d = bot._whoiscallbacks[nickname]

    d.addCallback(say_result)

    bot.msg(channel, "looking up %s" % (nickname))
    bot.whois(nickname)
