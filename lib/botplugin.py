# -*- coding: utf-8 -*-
import inspect
import re
from contextlib import contextmanager
from twisted.internet.task import LoopingCall
#from functools import wraps
# -*- coding: utf-8 -*-


class ExplicitReference(object):
    data = None


class StorageProxy(object):

    _default = {}

    def __init__(self, plugin):
        self.plugin = plugin

    @contextmanager
    def __call__(self, name, ref=False, default=None):
        d = ExplicitReference()
        try:
            d.data = self.plugin.factory.storage.get(self.plugin.name, name)
        except KeyError:
            if default is None:
                print "no default param"
                if not name in self._default.keys():
                    print "no default value"
                    raise
                d.data = self._default[name]
            else:
                d.data = default
        if ref:
            yield d.data
        else:
            yield d
        self.plugin.factory.storage.set(self.plugin.name, name, d.data)

    def setdefault(self, name, default):
        self.plugin.factory.storage.setdefault(self.plugin.name, name, default)
        self._default[name] = default


class BotPlugin(object):

    def __init__(self, core=False):
        self.factory = None
        self.stored = StorageProxy(self)
        self._handlers_msg = {}
        self._handlers_action = {}
        self._handlers_joined = {}
        self._handlers_init = []
        self._periodic = []
        (frame,
         filename,
         line_number,
         function_name,
         lines,
         index) = inspect.getouterframes(inspect.currentframe())[1]
        match = re.search(r'plugins/([^.]*)\.py', filename)
        if match:
            if core:
                self.name = "%s_%s" % (match.groups()[0], )
            else:
                self.name = match.groups()[0]
        else:
            raise    # BotException

    def bindto(self, factory):
        if self.factory is None:
            self.factory = factory
            for func in self._handlers_init:
                func()
        else:
            raise

    @contextmanager
    def stored(self, name, default=None):
        d = ExplicitReference()
        try:
            d.data = self.factory.storage.get(self.name, name)
        except KeyError:
            if default is None:
                raise
            d.data = default
        yield d
        self.factory.storage.set(self.name, name, d.data)

    @contextmanager
    def stored_ref(self, name, default=None):
        assert default is None \
            or isinstance(default, dict) \
            or isinstance(default, list)
        if self.factory.storage.exists(self.name, name):
            d = self.factory.storage.get(self.name, name)
        elif default is None:
            raise
        else:
            d = default
        yield d
        self.factory.storage.set(self.name, name, d)

    def check_permissions(self, handlername, user):
        with self.stored("__permissions__", default={}) as perms:
            if not handlername in perms.data:
                return 0
            return perms.data[handlername]

    ## Extenders - add functionality
    def add_any(self, f):
        self._handlers_msg[f.__name__] = f
        self._handlers_action[f.__name__] = f
        return f

    def add_joined(self, f):
        def wrapped(bot, user, channel):
            return f(bot, user, channel)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._handlers_joined[wrapped.__name__] = wrapped
        return wrapped

    def add_command(self, head, f):
        def wrapped(bot, user, channel, msg):
            if isinstance(head, list):
                headlist = head
            else:
                headlist = [head]
            for head_elem in headlist:
                if msg[0] in self.factory.config.commandchars:
                    msg1 = msg[1:].decode('utf-8')
                    if msg1.lower().startswith(head_elem.lower()):
                        msg1 = msg1[len(head_elem):]
                        return f(bot, user, channel, msg1.strip())
                elif msg.startswith(bot.nickname):
                    msg1 = msg[len(bot.nickname):].decode('utf-8')
                    msg1 = msg1.lstrip(self.factory.config.separators)
                    if msg1.lower().startswith(head.lower()):
                        msg1 = msg1[len(head):]
                        return f(bot, user, channel, msg1)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._handlers_msg[wrapped.__name__] = wrapped
        return wrapped

    def add_startswith(self, head, f):
        def wrapped(bot, user, channel, msg):
            if msg.lower().startswith(head.lower()):
                return f(bot, user, channel, msg)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._handlers_msg[wrapped.__name__] = wrapped
        return wrapped

    def add_contains(self, chunk, f):
        def wrapped(bot, user, channel, msg):
            if chunk.lower() in msg.lower():
                return f(bot, user, channel, msg)
        wrapped.__name__ = f.__name__
        wrapped.__doc__ = f.__doc__
        self._handlers_msg[wrapped.__name__] = wrapped
        return wrapped

    def callLater(self, seconds, function, *args, **kwargs):
        self.factory.reactor.callLater(seconds, function, *args, **kwargs)

    ## Decorators
    def init(self, f):
        self._handlers_init.append(f)
        return f

    def any(self, f):
        # use this decorator if you want to do something with ALL chat lines.
        # Example: Logging
        return self.add_any(f)

    def joined(self):
        # use this decorator if you want to be notified
        # when you joined a new channel
        def wrap(f):
            return self.add_joined(f)
        return wrap

    def command(self, head):
        # use to define a command. commands either start with a commandchar
        # (see config)
        # or with the name of the bot
        def wrap(f):
            return self.add_command(head, f)
        return wrap

    def startswith(self, head):
        # gets called for any line starting with head.
        def wrap(f):
            return self.add_startswith(head, f)
        return wrap

    def contains(self, chunk):
        # gets called for any line containing chunk
        def wrap(f):
            return self.add_contains(chunk, f)
        return wrap

    def periodic(self, seconds):
        # gets called every x seconds, float should be possible
        def wrap(f):
            lc = LoopingCall(f)
            lc.start(seconds)
            self._periodic.append(lc)
        return wrap

    def permission(self, level):
        def wrap(f):
            def setdefault():
                with self.stored_ref("__permissions__", default={}) as perms:
                    if not f.__name__ in perms:
                        perms[f.__name__] = level
            self._handlers_init.append(setdefault)
            return f
        return wrap

    ## helper methods
    # don't call these in plugins.
    # they are used by the bot mainloop to determine
    # if the message has any associated handlers
    def privmsghandler(self, bot, user, channel, msg):
        for func in self._handlers_msg.values():
            func(bot, user, channel, msg)

    def actionhandler(self, bot, user, channel, msg):
        for func in self._handlers_action.values():
            func(bot, user, channel, msg)

    def joinedhandler(self, bot, user, channel):
        for func in self._handlers_joined.values():
            func(bot, user, channel)
