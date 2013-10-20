# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import defer


class IRCBot(irc.IRCClient):

    # get names of users in channel
    # from http://stackoverflow.com/questions/6671620/list-users-in-irc-channel-using-twisted-python-irc-framework?lq=1
    def __init__(self, *args, **kwargs):
        self._namescallback = {}

    def names(self, channel):
        channel = channel.lower()
        d = defer.Deferred()
        if channel not in self._namescallback:
            self._namescallback[channel] = ([], [])

        self._namescallback[channel][0].append(d)
        self.sendLine("NAMES %s" % channel)
        return d

    def irc_RPL_NAMREPLY(self, prefix, params):
        channel = params[2].lower()
        nicklist = params[3].split(' ')

        if channel not in self._namescallback:
            return

        n = self._namescallback[channel][1]
        n += nicklist

    def irc_RPL_ENDOFNAMES(self, prefix, params):
        channel = params[1].lower()
        if channel not in self._namescallback:
            return

        callbacks, namelist = self._namescallback[channel]

        for cb in callbacks:
            cb.callback(namelist)

        del self._namescallback[channel]

    # end of names calls #

    def _get_nickname(self):
        if not hasattr(self, '_nickname'):
            self._nickname = self.factory.config.nickname
        return self._nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        print "Signed on as %s." % (self.nickname,)
        for channel in self.factory.config.channels:
            self.join(channel)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def nickChanged(self, nick):
        self._nickname = nick

    def msg(self, user, message, length=None):
        irc.IRCClient.msg(self, user, str(message), length)

    def action(self, user, channel, msg):
        self.factory.plugins.action(self, user, channel, msg)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""

        self.factory.plugins.privmsg(self, user, channel, msg)
        # for plugin in self.factory._plugins.values():
        #     plugin.privmsg(self, user, channel, msg)

    def callLater(self, seconds, function, *args, **kwargs):
        self.factory.reactor.callLater(seconds, function, *args, **kwargs)
