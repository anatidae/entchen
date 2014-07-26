# -*- coding: utf-8 -*-

from twisted.names import client, error, dns
from twisted.internet.task import react
from twisted.internet import defer
from twisted.python import usage


def lookup_host(bot, user, channel, msg, guess_best):
    hostname = msg
    if len(hostname):
        if guess_best:
            d = client.getHostByName(hostname)
            d.addCallback(resultCb, hostname, bot, channel)
            d.addErrback(errorCb, hostname, bot, channel)
        else:
            pending = []
            pending.append(client.lookupAddress(hostname))
            pending.append(client.lookupIPV6Address(hostname))
            allResults = defer.DeferredList(pending, consumeErrors=False)
            allResults.addCallback(resultCb, hostname, bot, user, channel)
            allResults.addErrback(errorCb, hostname, bot, user, channel)
    else:
        bot.msg(channel, 'Usage: !host <hostname>')


def resultCb(address, hostname, bot, user, channel):
    """
    Print the IP address or an error message if an IP address was not
    found.
    """
    msgs = []
    if not address:
        msgs.append('error: No IP found for {}'.format(hostname))
    elif isinstance(address, str):
        msgs.append('{} has address {}'.format(hostname, address))
    else:
        for result in address:
            if result[0]:  # success flag
                for rr in result[1][0]:
                    type_str = dns.QUERY_TYPES.get(rr.type)
                    if type_str == 'A':
                        msgs.append('{}: {}'.format(type_str, rr.payload.dottedQuad()))
                    else:
                        msgs.append('{}: {}'.format(type_str, rr.payload._address))
    target = channel
    if len(msgs) > 4:
        target = user
        bot.msg(channel, '{} resolves to {} entries. Sending them as query to {}.'
                .format(hostname, len(msgs), user.split('!', 1)[0]))
    for msg in msgs:
        bot.msg(target, msg)


def errorCb(failure, hostname, bot, user, channel):
    """
    Print a friendly error message if the hostname could not be
    resolved.
    """
    failure.trap(error.DNSNameError)
    bot.msg(channel, 'error: Hostname {} not found'.format(hostname))
