# coding=utf-8

from bot import BotPlugin
import random
import os.path
import shlex


chatter = BotPlugin()


def get_data_from_file(fn=None):
    """ Read data from file.

    Syntax:
    <key>=<value>
    """
    d = {}
    if not fn:
        fn = os.path.join(os.path.dirname(__file__),
                          'chatter.data')

    fp = open(fn)
    for line in fp.readlines():
        x = line.split('=')
        if len(x) > 1:
            d[x[0]] = x[1].strip()
    fp.close()
    return d


@chatter.init
def init(bot):
    chatter.stored.setdefault('keywordlines', get_data_from_file())


@chatter.command("chatter add")
def add_msg(bot, user, channel, msg):
    args = shlex.split(msg.encode('utf-8'))
    if len(args) > 1:
        keyword = args[0]
        line = " ".join(args[1:])
        with chatter.stored('keywordlines', True) as messages:
            messages[keyword] = line
            bot.msg(channel, "'%s': '%s' added" % (keyword, line))

@chatter.command("chatter del")
def del_msg(bot, user, channel, msg):
    args = shlex.split(msg.encode('utf-8'))
    if args:
        keyword = args[0]
        with chatter.stored('keywordlines', True) as messages:
            if keyword in messages:
                line = messages[keyword]
                del messages[keyword]
                bot.msg(channel, "'%s': '%s' deleted" % (keyword, line))
            else:
                bot.msg(channel, "%s was not in keywords" % (keyword, ))


@chatter.command("chatter list")
def list_msgs(bot, user, channel, msg):
    with chatter.stored('keywordlines', True) as messages:
        line = "', '".join(messages.keys())
        line = "'%s'" % line
        bot.msg(channel, line)


@chatter.any
def say_voicing(bot, user, channel, msg):
    if bot.nickname in msg and not msg.startswith(bot.nickname):
        l = ["quak", "quak", "schnatter", "quak quak"]
        bot.msg(channel, random.choice(l))


@chatter.any
def say_stuff(bot, user, channel, msg):
    with chatter.stored('keywordlines', True) as messages:
        for m in messages.keys():
            if m in msg.lower():
                import random
                msgs = messages.get(m, '').split(' | ')
                msg = msgs[random.randint(0, len(msgs)-1)]
                bot.msg(channel, msg)
