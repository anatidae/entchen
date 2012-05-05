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

for m in messages:
    chatter.add_contains(m, lambda bot, user, channel, msg: bot.msg(channel, messages.get(m)))
