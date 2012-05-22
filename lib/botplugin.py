# -*- coding: utf-8 -*-

class BotPlugin(object):

    def __init__(self):
        self.factory = None
        self._msghandlers = []

    ## Extenders - add functionality
    def add_any(self, f):
        self._msghandlers.append(f)
        return f

    def add_command(self, head, f):
        def wrapped(bot, user, channel, msg):
            if msg[0] in self.factory.config.commandchars:
                msg1 = msg[1:]
                if msg1.lower().startswith(head.lower()):
                    msg1 = msg1[len(head):]
                    f(bot, user, channel, msg1.strip())
            elif msg.startswith(bot.nickname):
                msg1 = msg[len(bot.nickname):]
                msg1 = msg1.lstrip(self.factory.config.separators)
                if msg1.lower().startswith(head.lower()):
                    msg1 = msg1[len(head):]
                    f(bot, user, channel, msg1)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._msghandlers.append(wrapped)
        return wrapped            

    def add_startswith(self, head, f):
        def wrapped(bot, user, channel, msg):
            if msg.lower().startswith(head.lower()):
                f(bot, user, channel, msg)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._msghandlers.append(wrapped)
        return wrapped            

    def add_contains(self, chunk, f):
        def wrapped(bot, user, channel, msg):
            if chunk.lower() in msg.lower():
                f(bot, user, channel, msg)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._msghandlers.append(wrapped)
        return wrapped
        
    ## Decorators
    def any(self, f):
        return self.add_any(f)
            
    def command(self, head):
        def wrap(f):
            return self.add_command(head, f)
        return wrap

    def startswith(self, head):
        def wrap(f):
            return self.add_startswith(head, f)
        return wrap

    def contains(self, chunk):
        def wrap(f):
            return self.add_contains(chunk, f)
        return wrap

    ## helper methods
    def privmsg(self, bot, user, channel, msg):
        for func in self._msghandlers:
            func(bot, user, channel, msg)

