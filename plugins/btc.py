from bot import BotPlugin
import requests

btc = BotPlugin()


@btc.command('btc')
def get_btc(bot, user, channel, msg):
    """
        Current bitcoin value on Mt. Gox.
        Usage: !btc [last|buy|sell|last_local|last_all|last_orig]
        default is last
    """
    args = msg.split()[0:]
    value_type = 'last'
    if len(args) > 0:
        if args[0] in ['last', 'buy', 'sell', 'last_local', 'last_all', 'last_orig']:
            value_type = args[0]
    usd = requests.get('http://data.mtgox.com/api/1/BTCUSD/ticker_fast')
    eur = requests.get('http://data.mtgox.com/api/1/BTCEUR/ticker_fast')
    m = u"\u0002MtGox\u000F (%s): %.2f USD - %.2f EUR" % (
        value_type,
        float(usd.json()['return'][value_type]['value']),
        float(eur.json()['return'][value_type]['value']),
    )
    bot.msg(channel, m)

