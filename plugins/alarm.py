from bot import BotPlugin
import datetime
import math

alarm = BotPlugin()

@alarm.command('nalarm')
def alarmcmd(bot, user, channel, msg):

    def showhelp():
        bot.msg(channel, "<time or minutes> <message>")

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

    sp = msg.split()
    if len(sp) < 2:
        showhelp()
        return

    if str(sp[0]).isdigit():
        seconds = int(sp[0]) * 60
    else:
        if ':' not in sp[0]:
            showhelp()
            return
        now = datetime.datetime.now()
        tm = [int(i) for i in sp[0].split(':')]
        x = datetime.datetime(now.year, now.month, now.day,
                              tm[0], tm[1])
        # calculate datetimedelta and save difference in seconds
        seconds = (x-now).seconds

    message = " ".join(sp[1:])
    username = user.split('!')[0]

    bot.factory.reactor.callLater(seconds, f, username, message)
    startmsg(username, seconds)
