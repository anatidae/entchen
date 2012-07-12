from bot import BotPlugin
import time
import os

gw = BotPlugin()

def get_gw_from_file(fn=None):
    """ Read data from file.

    Syntax:
    <nickname>=<todos>
    """
    d = {}
    if not fn:
        fn = os.path.join(os.path.dirname(__file__),
                          'gw.data')
    
    fp = open(fn)
    for line in fp.readlines():
        x = line.split('=')
        if len(x)>1:
            d[x[0]] = x[1].strip()
    fp.close()
    return d

@gw.command('gw')
def gw_command(bot, user, channel, msg):
    """ !gw <nick> <command> [<args>]
    default show
    """
    a = msg.split()
    nick = None
    cmd = ''

    if len(a)>0:
        d = get_gw_from_file()
        if a[0].lower() == 'list':
            m = 'Names: %s' % ', '.join(d.keys())
            bot.msg(channel, m)
            return

        nick = a[0]
        cmd = 'show'

    if len(a)>1:
        cmd = a[1]

    if cmd=='show':
        m = str(d.get(nick, ''))
#    elif cmd=='add'
#    elif cmd=='del'
    else:
        m = '!gw <nick> <command>'

    bot.msg(channel, m)
