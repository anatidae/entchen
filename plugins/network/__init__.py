# -*- coding: utf-8 -*-

from bot import BotPlugin

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
            return
        x = wh.get("status")
        if x:
            status = x[0]
        else:
            status = "unregistered"
        bot.msg(channel, "%s: %s" % (domain, status))
    else:
        bot.msg(channel, "usage: !whois <domain>")


@network.command('whois_verbose')
def say_whois_twisted(bot, user, channel, msg):

    from .whois import WhoisClient
    from twisted.internet import reactor

    client = WhoisClient(reactor, "whois.ripe.net")

    sp = msg.split()
    if len(sp) > 0:
        query = str(sp[0])
    else:
        bot.msg(channel, "usage: !whois_verbose <domain>")
        return

    d = client.query(query)
# --
    bot.msg(channel, "see query")
    usernick = user.split('!')[0]
    d.addCallback(lambda response: bot.msg(usernick, response))
    d.addErrback(lambda failure: bot.msg(usernick, str(failure)))
