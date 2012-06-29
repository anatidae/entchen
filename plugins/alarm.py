from bot import BotPlugin
import datetime
import math

alarm = BotPlugin()

@alarm.command('nalarm')
def alarmcmd(bot, user, channel, msg):
    """ alarm is the German name for remind.
    """

    # TODOs:
    # - save all reminders in the factory for a !showalarms command
    # - maybe: add !delalarm <alarmid>

    def showhelp():
        bot.msg(channel, "[<nick>] <time or minutes> <message>")

    def startmsg(username, seconds):
        minutes = math.floor(seconds / 60)
        pl = ''
        if minutes != 1:
            pl = 's'
        m = "Reminding %s in %i minute%s: %s" % (username, minutes, pl, message)
        bot.msg(channel, m)


    def f(username, s):
        m = "%s: --- %s ---" % (username, s)
        bot.msg(channel, m)

    # FIXME: best way to get the username?
    username = user.split('!')[0]
    message = None
    seconds = None

    sp = msg.split()
    if len(sp) < 2:
        showhelp()
        return

    timevalue = sp[0]

    if str(timevalue).isdigit():
        seconds = int(timevalue) * 60
    else:
        if ':' not in timevalue:
            timevalue = sp[1]
            if ':' in timevalue or str(timevalue).isdigit():
                if str(timevalue).isdigit():
                    seconds = int(timevalue) * 60
                # <user> <time> <message>
                username = sp[0]
                timevalue = sp[1]
                message = " ".join(sp[2:])
            else:
                showhelp()
                return
        if not seconds:
            now = datetime.datetime.now()
            tm = [int(i) for i in timevalue.split(':')]
            x = datetime.datetime(now.year, now.month, now.day,
                                  tm[0], tm[1])
            # calculate datetimedelta and save difference in seconds
            seconds = (x-now).seconds

    if not message:
        message = " ".join(sp[1:])

    bot.factory.reactor.callLater(seconds, f, username, message)
    startmsg(username, seconds)
