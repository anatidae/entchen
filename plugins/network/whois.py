# -*- coding: utf-8 -*-

from twisted.internet import defer
from twisted.internet.protocol import (
    connectionDone,
    ClientCreator,
    Protocol,
)


class WhoisClientProtocol(Protocol):
    """Basic Whois Protocol following RFC3912
    """

    _buffer = None

    def __init__(self, query, finisher):
        self.query = query
        self.finisher = finisher

    def connectionMade(self):
        self._buffer = []
        self.transport.write(self.query + "\r\n")

    def dataReceived(self, data):
        self._buffer.append(data)

    def connectionLost(self, reason=connectionDone):
        if self._buffer:
            self.finisher.callback(''.join(self._buffer))
        else:
            # TODO: if self._waiting NoResponse
            self.finisher.errback(reason)


class WhoisClient(object):
    """Implementation of whois client
    """

    _protocol = WhoisClientProtocol
    _port = 43

    def __init__(self, reactor, host, port=None):
        self._reactor = reactor
        self._host = host
        self._port = port or self._port

    def _connect(self, *proto_args):
        cc = ClientCreator(self._reactor, self._protocol, *proto_args)
        return cc.connectTCP(self._host, self._port)

    def query(self, query):
        d = defer.Deferred()

        # get whois server from file
        import os.path
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whois_server_list')
        self._host = get_host_from_file(fn, query)

        self._connect(query, d)
        return d


def get_host_from_file(filename, domain):
    # get tld:
    if not '.' in domain:
        raise ValueError('domain has no tld')
    tld = domain.split('.')[-1]
    with open(filename) as fp:
        for line in fp:
            if line.startswith('#'):
                continue
            x = line.split(' ')
            if len(x) > 1:
                if x[0] == tld:
                    return x[1].strip()
    return "whois.ripe.net"
