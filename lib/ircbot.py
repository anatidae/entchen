# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import defer


class IRCBot(irc.IRCClient):

    # get names of users in channel
    # from http://stackoverflow.com/questions/6671620/list-users-in-irc-channel-using-twisted-python-irc-framework?lq=1
    def __init__(self, *args, **kwargs):
        self._namescallback = {}
        self._whoiscallbacks = {}

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

    def irc_330(self, prefix, params):
        """
        this is a part of the whois reply
        it has to be handled asynchronously since this receiver
        has no info about where, how or why the whois was requested

        on Freenode, this is a message in this form:
        :prefix: the name of the IRC server you are connected to
        :params: a list in this form:
          [YOURNAME, HISNAME, HISNICKSERVNAME, MESSAGE]
        the MESSAGE is plaintext
        the string you would see in your client would be
        HISNAME MESSAGE HISNICKSERVNAME

        example params:
        ['entchen', 'Jon', 'JonDoe', 'is logged in as']
        which would be displayed as "Jon is logged in as JonDoe"
        by an IRC client
        """
        if len(params) == 4:
            nickname = params[1]
            if nickname in self._whoiscallbacks:
                if params[3] == 'is logged in as':
                    account = params[2]
                    self._whoiscallbacks[nickname].callback(account)
                else:
                    self._whoiscallbacks[nickname].callback(False)
                del self._whoiscallbacks[nickname]
        print """received 330 prefix "%s" params "%s" """ % (prefix, params)

    def irc_unknown(self, prefix, command, params):
        """
        this is a fallback event handler which gets called for all events
        we don't handle. All other irc_* methods take precedence.
        """

        #TODO: only print this in debug mode? command line switch?
        print 'received unknown prefix "%s" command "%s" params "%s"' % (
            prefix, command, params
        )

    def _get_nickname(self):
        if not hasattr(self, '_nickname'):
            self._nickname = self.factory.config.nickname
        return self._nickname
    nickname = property(_get_nickname)

    def msg(self, user, message, length=None):
        if isinstance(message, unicode):
            message = unicode(message).encode("utf-8")
        irc.IRCClient.msg(self, user, message, length)

    ## Listeners - these get called by the bot when an event happens
    def signedOn(self):
        print "Signed on as %s." % (self.nickname,)
        for channel in self.factory.config.channels:
            self.join(channel)

        # Give the factory access to the bot
        # This breaks the multi bot design... but it's alread broken
        self.factory.bot = self

    def joined(self, channel):
        print "Joined %s." % (channel,)
        self.factory.plugins.joined(self, channel)

    def userJoined(self, user, channel):
        self.factory.plugins.userJoined(self, user, channel)

    def nickChanged(self, nick):
        self._nickname = nick

    def action(self, user, channel, msg):
        self.factory.plugins.action(self, user, channel, msg)

    def privmsg(self, user, channel, msg):
        self.factory.plugins.privmsg(self, user, channel, msg)

    def callLater(self, seconds, function, *args, **kwargs):
        self.factory.reactor.callLater(seconds, function, *args, **kwargs)
