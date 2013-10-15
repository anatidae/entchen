from bot import BotPlugin

sysinfo = BotPlugin()


def parse_meminfo():
    m = {}
    f = open('/proc/meminfo')
    while True:
        l = f.readline()
        if not l:
            break
        (key, value) = l.split(':')
        m[key.strip()] = value.strip()
    return m


@sysinfo.command('mem')
def meminfo(bot, user, channel, msg):
    meminfo = parse_meminfo()
    (total, tunit) = meminfo['MemTotal'].split()
    (free, funit) = meminfo['MemFree'].split()
    total = int(total)
    free = int(free)
    usedp = float(total-free)/float(total)*100.0
    if tunit == funit:
        if tunit == "kB":
            bot.msg(channel,
                    "Memory usage: %.2f%% total: %s mB free: %s mB"%
                    (usedp, total/1024, free/1024))
        else:
            bot.msg(channel,
                    "Memory usage: %.2f%% total: %s %s free: %s %s"%
                    (usedp, total, tunit, free/1024, funit))
