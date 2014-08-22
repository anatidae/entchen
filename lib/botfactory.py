# -*- coding: utf-8 -*-

from twisted.internet import protocol
from ircbot import IRCBot
from botstorage import BotStorage, BotConfigWrapper
#import sys
#import traceback
import importlib


class BotFactory(protocol.ClientFactory):
    protocol = IRCBot

    def __init__(self, config, reactor, webresource=None):
        self.storage = BotStorage(config.storage)
        self.config = BotConfigWrapper(self.storage, config)
        self.reactor = reactor
        self.webresource = webresource

        self.plugins = importlib.import_module('lib.pluginloader')
        self.plugins._init_plugins(self)

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
