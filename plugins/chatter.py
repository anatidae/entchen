from bot import BotPlugin

chatter = BotPlugin()

messages = {}
messages['fool'] = 'zu Recht.'
messages['#uasy'] = 'YEAH!'
messages['feuer'] = "Getadelt wird wer Schmerzen kennt | " \
    "Vom Feuer das die Haut verbrennt | Ich werf ein Licht " \
    "| In mein Gesicht | Ein heisser Schrei | Feuer Frei! "
messages['sonne'] = "Hier kommt die Sonne."
messages['kaffee'] = "Da bin ich dabei!"

for m in messages.keys():
    reply = messages.get(m)

    def tmp(bot, user, channel, msg):
        bot.msg(channel, reply)
    tmp.__name__ = "say_%s"%m
    chatter.add_contains(m, tmp)

chatter.add_contains('blub', lambda bot, user, channel, msg: bot.msg(channel, 'blah'))
