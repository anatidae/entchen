import traceback
from botplugin import BotPlugin
#import importlib
import imp

_loaded = []
try:
    _loaded = _plugins.keys()
except NameError:
    _plugins = {}

try:
    _factory
except NameError:
    _factory = None


def add_plugin(plugin, override = False, reraise=False):
    global _plugins
    global _factory
    name = plugin
    if name in _plugins and not override:
        print "Plugin named %s already loaded"%name
        return
    try:
        plugins = imp.load_module('plugins', *imp.find_module('plugins'))
        pluginmod = imp.load_module(plugin, *imp.find_module(plugin, plugins.__path__))
        plugin = getattr(pluginmod, plugin)
        # pluginmod = importlib.import_module('plugins.%s' % (name, ))
        # plugin = getattr(pluginmod, plugin)
    except:
        #e = sys.exc_info()[0]
        if reraise:
            raise
        return traceback.format_exc()
    if isinstance(plugin, BotPlugin):
        if plugin.factory and not override:
            print "Plugin already assigned to a bot, can't reassign"
            return
        plugin.factory = _factory
        _plugins[name] = plugin
    return ""

def del_plugin(plugin):
    global _plugins
    if plugin in _plugins:
        del _plugins[plugin]

def reload_plugin(plugin):
    global _plugins
    if plugin in _plugins:
        return add_plugin(plugin, True)

def reload_plugins(plugins=None):
    global _plugins
    if not plugins:
        plugins = _plugins.keys()
    errors = ""
    badplugs = []
    for plugin in plugins:
        error = add_plugin(plugin, True)
        if error:
            badplugs.append(plugin)
            errors += error
    return (badplugs, errors)

def reload_self(bot, user, channel):
    global _bot
    global _channel
    global _user
    global _factory

    # set variables that we need after the reload
    _bot = bot
    _user = user
    _channel = channel
    reload(_factory.plugins)

if _loaded:  # only entered after reload
    _bot.msg(_channel, 'reloading all plugins')
    (badplugs, errors) = reload_plugins(_loaded)
    if errors:
        _bot.msg(channel,
                "failed to reload plugin(s) %s; see query"%
                ', '.join(badplugs))
        _bot.msg(_user, errors)
    # we don't want those temporary variables anymore
    del _channel
    del _user
    del _bot
del _loaded

def privmsg(bot, user, channel, msg):
    global _plugins
    global _factory
    if msg.startswith('!reload'):
        args = msg.split()[1:]
        if len(args) > 0:
            bot.msg(channel, 'reloading %s'%', '.join(args))
            for arg in args:
                error = reload_plugin(arg)
                if error:
                    bot.msg(channel, 'error loading %s, see query'%arg)
                    bot.msg(user, error)
        else:
            bot.msg(channel, 'reloading plugin loader')
            reload_self(bot, user, channel)
        return
    if msg.startswith('!load'):
        args = msg.split()[1:]
        if len(args) > 0:
            bot.msg(channel, 'loading %s'%', '.join(args))
            for arg in args:
                error = add_plugin(arg)
                if error:
                    bot.msg(channel, 'error loading %s, see query'%arg)
                    bot.msg(user, error)
        else:
            bot.msg(channel, 'load needs one or more plugins to be loaded')
        return
    if msg.startswith('!unload'):
        args = msg.split()[1:]
        if len(args) > 0:
            bot.msg(channel, 'unloading %s'%', '.join(args))
            for arg in args:
                del_plugin(arg)
        else:
            bot.msg(channel, 'unload needs one or more plugins to be unloaded')
        return
    if msg.startswith('!plugins'):
        args = msg.split()[1:]
        if len(args) == 0:
            keys = sorted(_plugins.keys())

            bot.msg(channel,
                    'Plugins loaded: %s'%
                    (' '.join(keys),))
        elif args[0] == "save":
            _factory.config.plugins = _plugins.keys()
            bot.msg(channel, 'Plugins saved')
    if msg.startswith('!join'):
        args = msg.split()[1:]
        if len(args) > 0:
            for arg in args:
                bot.join(arg)
    if msg.startswith('!part'):
        args = msg.split()[1:]
        if len(args) > 0:
            for arg in args:
                bot.part(arg)
        else:
            bot.part(channel)

    for plugin in _plugins.values():
        plugin.privmsg(bot, user, channel, msg)

def _init_plugins(factory):
    global _plugins
    global _factory
    _factory = factory

    for plugin in _factory.config.plugins:
        add_plugin(plugin, reraise=True)
