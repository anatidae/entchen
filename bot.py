# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor, ssl
import sys, os
import random
import time
import subprocess
import imp

class Config:
    nickname = 'entchen'
    server = '188.40.78.73'
    channel = '#cl-study'

class TestConfig:
    nickname = 'testchen'
    server = '188.40.78.73'
    channel = '#test'

class BotPlugin(object):

    def __init__(self, bot = None):
        self.factory = None
        self._msghandlers = []

    ## Extenders - add functionality
    def add_startswith(self, head, f):
        def wrapped(bot, user, channel, msg):
            if msg.lower().startswith(head.lower()):
                f(bot, user, channel, msg)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._msghandlers.append(wrapped)
        return wrapped            

    def add_contains(self, chunk, f):
        def wrapped(bot, user, channel, msg):
            if chunk.lower() in msg.lower():
                f(bot, user, channel, msg)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._msghandlers.append(wrapped)
        return wrapped
        
    ## Decorators
    def startswith(self, head):
        def wrap(f):
            return self.add_startswith(head, f)
        return wrap

    def contains(self, chunk):
        def wrap(f):
            return self.add_contains(chunk, f)
        return wrap

    ## helper methods
    def privmsg(self, bot, user, channel, msg):
        for func in self._msghandlers:
            func(bot, user, channel, msg)

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

        messages = {}
        messages['fool'] = 'zu Recht.'
        messages['#uasy'] = 'YEAH!'
        messages['feuer'] = "Getadelt wird wer Schmerzen kennt | " \
            "Vom Feuer das die Haut verbrennt | Ich werf ein Licht " \
            "| In mein Gesicht | Ein heisser Schrei | Feuer Frei! "
        messages['sonne'] = "Hier kommt die Sonne."
        messages['kaffee'] = "Da bin ich dabei!"

        for m in messages.keys():
            if m in msg.lower():
                self.msg(channel, messages.get(m))

        if msg.startswith("!date"):
            m = "Date: %s" % time.strftime("%a, %b %d, %Y", time.localtime())
            self.msg(channel, m)

        if msg.startswith("!head"):

            # TODO: check if branch exists
            # TODO: cleanup

            sp = msg.split()
            branch = 'master'
            if len(sp)>1:
                repo = sp[1]
            else:
                repo = ''
            if len(sp)>2:
                branch = sp[2]

            if repo == 'entchen':
                m = self.git_head('/admin/verwaltung/repository/entchen.git/', 
                                  branch)
            elif repo == 'voliere':
                m = self.git_head('/admin/verwaltung/repository/verwaltung.git/',
                                  branch)
            elif repo == 'issues':
                m = self.git_head('/admin/verwaltung/repository/issues.git/', 
                                  branch)
            else:
                m = 'give name of repo (i.e. entchen, voliere)'
            self.msg(channel, m)

        for plugin in self.factory._plugins.values():
            plugin.privmsg(self, user, channel, msg)

    def git_head(self, folder, branch='master'):
        m = subprocess.Popen('cd %s; git log %s --pretty=format:"%%h >>>%%s<<< [%%aN]" HEAD -n 1' \
                                 % (folder, branch),
                             shell=True, stdout=subprocess.PIPE).stdout
        return m.read()


class EntchenBotFactory(protocol.ClientFactory):
    protocol = EntchenBot

    def __init__(self, channel, nickname):
        self.channel = channel
        self.nickname = nickname
        self._plugins = {}

    def add_plugin(self, plugin, override = False):
        name = plugin
        if name in self._plugins and not override:
            print "Plugin named %s already loaded"%name
            return
        plugins = imp.load_module('plugins', *imp.find_module('plugins'))
        pluginmod = imp.load_module(plugin, *imp.find_module(plugin, plugins.__path__))
        plugin = getattr(pluginmod, plugin)
        from bot import BotPlugin # voodoo, next line won't work without this obnoxious import
        if isinstance(plugin, BotPlugin):
            if plugin.bot and not override:
                print "Plugin already assigned to a bot, can't reassign"
                return
            plugin.bot = self
            self._plugins[name] = plugin
            
    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)


if __name__ == "__main__":

    if len(sys.argv)>1 and sys.argv[1] == 'testing':
        c = TestConfig()
    else:
        c = Config()

    reactor.connectSSL(c.server,
                       6668, 
                       EntchenBotFactory(channel=c.channel,
                                         nickname=c.nickname),
                       ssl.ClientContextFactory())

    reactor.run()
