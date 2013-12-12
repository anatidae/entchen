from bot import BotPlugin
import requests

btc = BotPlugin()


@btc.command('btc')
def get_btc(bot, user, channel, msg):
    usd = requests.get('http://data.mtgox.com/api/1/BTCUSD/ticker_fast')
    eur = requests.get('http://data.mtgox.com/api/1/BTCEUR/ticker_fast')
    m = u"\u0002MtGox\u000F: %.2f USD - %.2f EUR" % (
        float(usd.json()['return']['last']['value']),
        float(eur.json()['return']['last']['value'])
    )
    bot.msg(channel, m)

