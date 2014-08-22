# -*- coding: utf-8 -*-

# try:
#     import geventreactor
#     geventreactor.install()
#     print "gevent reactor found!"
# except ImportError:
#     print "no gevent :( (pip install geventreactor)"
#     pass

from lib.botplugin import BotPlugin
from lib.ircbot import IRCBot
from lib.botfactory import BotFactory
import logging


logging.basicConfig()


class Bot(object):

    def __init__(self, config=False):
        self.config = config
        self.webresource = None
        self.factory = None

        from twisted.internet import reactor
        self.reactor = reactor

    def set_config(self, config):
        if not self.config:
            self.config = config

    def _init_factory(self):
        if not self.config:
            raise Exception("No config for BotFactory avaiable")

        if hasattr(self.config, 'webserver') and self.config.webserver:
            from twisted.web.resource import Resource
            self.webresource = Resource()

        self.factory = BotFactory(
            config=self.config, reactor=self.reactor,
            webresource=self.webresource
        )

    def run(self):
        if not self.factory:
            self._init_factory()

        if self.config and self.factory and self.reactor:
            if self.config.ssl:
                from twisted.internet import ssl
                self.reactor.connectSSL(
                    self.config.server, self.config.port,
                    self.factory, ssl.ClientContextFactory()
                )
            else:
                self.reactor.connectTCP(
                    self.config.server, self.config.port, self.factory
                )

            # Activate webservice
            if self.webresource is not None:
                from twisted.web.server import Site

                site_factory = Site(self.webresource)
                self.reactor.listenTCP(
                    self.config.webserver_port, site_factory
                )

            # Add sentry error handler
            if hasattr(self.config, 'sentry_dsn'):
                from twisted.python import log
                from raven.handlers.logging import SentryHandler
                self.sentry = SentryHandler(self.config.sentry_dsn)

                logging.getLogger('twisted').addHandler(self.sentry)
                self.observer = log.PythonLoggingObserver()
                self.observer.start()

            self.reactor.run()

bot = Bot()
