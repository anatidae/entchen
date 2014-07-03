from bot import BotPlugin

channel = BotPlugin()


@channel.command('join')
def join(bot, user, channel, msg):
    """
    Join a channel:

    join <channel> [<channel> ...]
    """
    args = msg.split()
    if msg and len(args) > 0:
        for arg in args:
            bot.join(str(arg))
            bot.msg(channel, 'Joined %s' % arg)


@channel.command('part')
def part(bot, user, channel, msg):
    """
    Leave a channel:

    part <channel> [<channel> ...]
    """
    args = msg.split()
    if msg and len(args) > 0:
        for arg in args:
            bot.part(str(arg))
    else:
        bot.msg(channel, 'Bye')
        bot.part(str(channel))


@channel.command('channel remember')
def remember(bot, user, channel, msg):
    """
    Join and remember to rejoin a channel:

    channel remember <channel> [<channel> ...]
    """
    args = msg.split()
    if msg and len(args) > 0:
        new_channels = []
        channels = bot.factory.config.channels
        for arg in args:
            current = str(arg)
            bot.join(current)
            if current not in channels:
                new_channels.append(current)
        channels.extend(new_channels)
        bot.factory.config.channels = channels
        bot.msg(channel,
                'Remembering to rejoin %s' %
                ', '.join(new_channels))


@channel.command('channel forget')
def forget(bot, user, channel, msg):
    """
    Part and forget to rejoin a channel:

    channel forget <channel> [<channel> ...]
    """
    args = msg.split()
    if msg and len(args) > 0:
        parted_channels = []
        channels = bot.factory.config.channels
        for arg in args:
            current = str(arg)
            if current == channel:
                #don't part the channel this command was invoked in
                continue
            bot.part(current)
            if current in channels:
                parted_channels.append(current)
        print "old", channels
        channels = [x for x
                    in channels
                    if x not in parted_channels]
        print "new", channels
        bot.factory.config.channels = channels
        bot.msg(channel,
                'Forgetting to rejoin %s' %
                ', '.join(parted_channels))
