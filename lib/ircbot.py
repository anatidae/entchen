# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
import random

class IRCBot(irc.IRCClient):
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
                (badplugs, errors) = self.factory.reload_plugins()
                if errors:
                    self.msg(channel,
                             "failed to reload plugin(s) %s; see query"%
                             ', '.join(badplugs))
                    self.msg(user, errors)
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
        if msg.startswith('!plugins'):
            keys = self.factory._plugins.keys()
            
            self.msg(channel,
                     'Plugins loaded: %s'%
                     (' '.join(keys),))
#            [plugin for plugin in 
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

