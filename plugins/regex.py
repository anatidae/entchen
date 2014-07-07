# -*- coding: utf-8 -*-
from bot import BotPlugin
import re

regex = BotPlugin()
search_re = re.compile(r'(?:^|\s)s/([^/]+)/([^/]*)/([gi]*)(?:\s|$)')
match_re = re.compile(r'^([^\s]+):\s+s/([^/]+)/([^/]*)/([gi]*)$')
lastline = {}


def dosub(orig, repl, line, flags):
    f = 0
    count = 1
    if "i" in flags:
        f = re.I
    if "g" in flags:
        count = 0
    line2 = re.sub(orig, repl, line, count, f)
    if line2 != line:
        return line2
    return False

@regex.any
def find_regex(bot, user, channel, msg):
    user = user.split('!')[0]
    match = match_re.match(msg)
    if match:
        (user2, orig, repl, flags) = match.groups()
        line = lastline.get((user2, channel))
        if not line:
            return
        line = dosub(orig, repl, line, flags)
        if line:
            bot.msg(channel, "%s did you mean: %s" % (user2, line))
        return

    match = search_re.search(msg)
    if match:
        line = lastline.get((user, channel))
        if not line:
            return
        (orig, repl, flags) = match.groups()
        line = dosub(orig, repl, line, flags)
        if line:
            bot.msg(channel, "%s meant: %s" % (user, line))
    else:
        lastline[(user, channel)] = msg
