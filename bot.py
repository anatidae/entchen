# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor, ssl
import sys
import random
import imp
import traceback

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
    def add_any(self, f):
        self._msghandlers.append(f)
        return f
        
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
    def any(self, f):
        return self.add_any(f)
            
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
        
        if msg.startswith('!reload'):
            args = msg.split()[1:]
            if len(args) > 0:
                self.msg(channel, 'reloading %s'%', '.join(args))
                for arg in args:
                    error = self.factory.reload_plugin(arg)
                    if error:
                        self.msg(channel, 'error loading %s, see query'%arg)
                        self.msg(user, error)
            else:
                self.msg(channel, 'reloading all plugins')
                error = self.factory.reload_plugins()
                if error:
                    self.msg(channel, "failed to reload plugin(s) %s; see query"%', '.join(error[0]))
                    self.msg(user, error[1])
            return
        if msg.startswith('!load'):
            args = msg.split()[1:]
            if len(args) > 0:
                self.msg(channel, 'loading %s'%', '.join(args))
                for arg in args:
                    error = self.factory.add_plugin(arg)
                    if error:
                        self.msg(channel, 'error loading %s, see query'%arg)
                        self.msg(user, error)
            else:
                self.msg(channel, 'load needs one or more plugins to be loaded')
            return
        if msg.startswith('!unload'):
            args = msg.split()[1:]
            if len(args) > 0:
                self.msg(channel, 'unloading %s'%', '.join(args))
                for arg in args:
                    self.factory.del_plugin(arg)
            else:
                self.msg(channel, 'unload needs one or more plugins to be unloaded')
            return
        if msg.startswith('!join'):
            args = msg.split()[1:]
            if len(args) > 0:
                for arg in args:
                    self.join(arg)
        if msg.startswith('!part'):
            args = msg.split()[1:]
            if len(args) > 0:
                for arg in args:
                    self.part(arg)
            else:
                self.part(channel)
        
        if self.nickname in msg:
            l = ["quak","quak","schnatter","quak quak"]
            self.msg(channel, random.choice(l))
            
        for plugin in self.factory._plugins.values():
            plugin.privmsg(self, user, channel, msg)

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
        try:
            plugins = imp.load_module('plugins', *imp.find_module('plugins'))
            pluginmod = imp.load_module(plugin, *imp.find_module(plugin, plugins.__path__))
            plugin = getattr(pluginmod, plugin)
        except:
            e = sys.exc_info()[0]
            return traceback.format_exc()
        from bot import BotPlugin # voodoo, next line won't work without this obnoxious import
        if isinstance(plugin, BotPlugin):
            if plugin.factory and not override:
                print "Plugin already assigned to a bot, can't reassign"
                return
            plugin.factory = self
            self._plugins[name] = plugin
        return ""
            
    def del_plugin(self, plugin):
        if plugin in self._plugins:
            del self._plugins[plugin]

    def reload_plugin(self, plugin):
        if plugin in self._plugins:
            return self.add_plugin(plugin, True)

    def reload_plugins(self):
        error = ""
        badplugs = []
        for plugin in self._plugins:
            error += self.add_plugin(plugin, True)
            badplugs.append(plugin)
        return (badplugs, errors)

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
        
    factory = EntchenBotFactory(channel=c.channel,
                                nickname=c.nickname)
    factory.add_plugin('chatter')
#    print factory._plugins['chatter']._msghandlers
#    factory._plugins['chatter']._msghandlers[0](None, None, None, 'fool')
    factory.add_plugin('date')
    factory.add_plugin('git')

    reactor.connectSSL(c.server,
                       6668, 
                       factory,
                       ssl.ClientContextFactory())

    reactor.run()
