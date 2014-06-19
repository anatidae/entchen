from bot import BotPlugin
import time
import socket

network = BotPlugin()


@network.command('ping')
def say_pong(bot, user, channel, msg):
    """ print pong
    """
    bot.msg(channel, 'pong')


@network.command('whois')
def say_whois(bot, user, channel, msg):
    """ whois for domain given as parameter
    """
    import pythonwhois

    sp = msg.split()
    if len(sp) > 0:
        domain = sp[0]
        print domain
        try:
            wh = pythonwhois.get_whois(domain)
        except Exception as e:
            bot.msg(channel, repr(e))
        x = wh.get("status")
        if x:
            status = x[0]
        else:
            status = "unregistered"
        bot.msg(channel, "%s: %s" % (domain, status))
    else:
        bot.msg(channel, "usage: !whois <domain>")
