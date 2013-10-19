# -*- coding: utf-8 -*-

from twisted.internet import protocol
from ircbot import IRCBot
from botplugin import BotPlugin
from botstorage import BotStorage, BotConfigWrapper
import sys
import traceback
import importlib

class BotFactory(protocol.ClientFactory): #REFACTOR needs a generic name
    protocol = IRCBot

    def __init__(self, config, reactor):
        self.storage = BotStorage(config.storage)
        self.config = BotConfigWrapper(self.storage, config)
        self.reactor = reactor
        self._init_plugins()

    def _init_plugins(self):
        self._plugins = {}
        for plugin in self.config.plugins:
            self.add_plugin(plugin, reraise=True)

    def add_plugin(self, plugin, override = False, reraise=False):
        name = plugin
        if name in self._plugins and not override:
            print "Plugin named %s already loaded"%name
            return
        try:
            pluginmod = importlib.import_module('plugins.%s' % (name, ))
            plugin = getattr(pluginmod, plugin)
        except:
            #e = sys.exc_info()[0]
            if reraise:
                raise
            return traceback.format_exc()
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
        errors = ""
        badplugs = []
        for plugin in self._plugins:
            error = self.add_plugin(plugin, True)
            if error:
                badplugs.append(plugin)
                errors += error
        return (badplugs, errors)

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
