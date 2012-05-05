from bot import BotPlugin
import copy

chatter = BotPlugin()

@chatter.any
def say_stuff(bot, user, channel, msg):
    messages = {}
    messages['fool'] = 'zu Recht.'
    messages['#uasy'] = 'YEAH!'
    messages['feuer'] = "Getadelt wird wer Schmerzen kennt | " \
        "Vom Feuer das die Haut verbrennt | Ich werf ein Licht " \
        "| In mein Gesicht | Ein heisser Schrei | Feuer Frei! "
    messages['sonne'] = "Hier kommt die Sonne."
    messages['kaffee'] = "Da bin ich dabei!"

    for m in messages.keys():
        if m in msg.lower():
            bot.msg(channel, messages.get(m))
