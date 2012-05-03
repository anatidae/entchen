# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor, ssl
import sys
import random
import time
import subprocess

class Config:
    nickname = 'entchen'
    server = '188.40.78.73'
    channel = '#cl-study'

class TestConfig:
    nickname = 'testchen'
    server = '188.40.78.73'
    channel = '#test'


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
