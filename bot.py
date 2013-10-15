# -*- coding: utf-8 -*-

from lib.botplugin import BotPlugin
from lib.ircbot import IRCBot
from lib.botfactory import BotFactory


class Bot:
    def __init__(self, config=False):
        self.config = config
        self._init_factory()
        from twisted.internet import reactor
        self.reactor = reactor

    def _init_factory(self):
        if self.config:
            self.factory = BotFactory(config=self.config, reactor=self.reactor)

    def set_config(self, config):
        if not self.config:
            self.config = config
            self._init_factory()

    def run(self):
        if self.config and self.factory and self.reactor:
            if self.config.ssl:
                from twisted.internet import ssl
                self.reactor.connectSSL(self.config.server,
                                        self.config.port,
                                        self.factory,
                                        ssl.ClientContextFactory())
            else:
                self.reactor.connectTCP(self.config.server,
                                        self.config.port,
                                        self.factory)
            self.reactor.run()

bot = Bot()
