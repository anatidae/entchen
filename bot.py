# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor, ssl
import sys
import random
import time

class EntchenBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""

        if self.nickname in msg:
            l = ["quak","quak","schnatter","quak quak"]
            self.msg(channel, random.choice(l))

        if "fool" in msg.lower():
            self.msg(channel, "zu Recht.")
        
        if "#uasy" in msg.lower():
            self.msg(channel, "YEAH!")

        if "feuer" in msg.lower():
            m = "Getadelt wird wer Schmerzen kennt | Vom Feuer das die Haut verbrennt | Ich werf ein Licht | In mein Gesicht | Ein heisser Schrei | Feuer Frei! "
            self.msg(channel, m)

        if "sonne" in msg.lower():
            self.msg(channel, "Hier kommt die Sonne.")

        if "kaffee" in msg.lower():
            self.msg(channel, "Da bin ich dabei!")

        if msg.startswith("!date"):
            m = "Date: %s" % time.strftime("%a, %b %d, %Y", time.localtime())
            self.msg(channel, m)


class EntchenBotFactory(protocol.ClientFactory):
    protocol = EntchenBot

    def __init__(self, channel, nickname='entchen'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)


if __name__ == "__main__":

    reactor.connectSSL('188.40.78.73', 6668, EntchenBotFactory('#cl-study'),
                       ssl.ClientContextFactory())

    reactor.run()
