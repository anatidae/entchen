# -*- coding: utf-8 -*-
import sys
import inspect
import re
from contextlib import contextmanager


class ExplicitReference(object):
    data = None


class BotPlugin(object):

    def __init__(self):
        self.factory = None
        self._msghandlers = []
        frame,filename,line_number,function_name,lines,index = inspect.getouterframes(inspect.currentframe())[1]
        match = re.search(r'plugins/([^.]*)\.py', filename)
        if match:
            self.name = match.groups()[0]
        else:
            raise    # BotException

    @contextmanager
    def stored(self, name, default=None):
        d = ExplicitReference()
        try:
            d.data = self.factory.storage.get(self.name, name)
        except KeyError, e:
            if default is None:
                raise
            d.data = default
        yield d
        self.factory.storage.set(self.name, name, d.data)

    ## Extenders - add functionality
    def add_any(self, f):
        self._msghandlers.append(f)
        return f

    def add_command(self, head, f):
        def wrapped(bot, user, channel, msg):
            if isinstance(head, []):
                headlist = head
            else:
                headlist = [head]
            for head_elem in headlist:
                if msg[0] in self.factory.config.commandchars:
                    msg1 = msg[1:].decode('utf-8')
                    if msg1.lower().startswith(head_elem.lower()):
                        msg1 = msg1[len(head_elem):]
                        f(bot, user, channel, msg1.strip())
                elif msg.startswith(bot.nickname):
                    msg1 = msg[len(bot.nickname):].decode('utf-8')
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
    def init(self, f):
        f()
        return f

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
