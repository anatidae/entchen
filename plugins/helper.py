# -*- coding: utf-8 -*-
from bot import BotPlugin
from lib.pluginloader import get_plugin, _plugins, _factory

helper = BotPlugin()


@helper.command('help')
def help(bot, user, channel, msg):
    """help <plugin> [<command>] - Show help for plugin/command"""
    args = msg.split(' ', 2)[0:]
    if len(args) == 1 and args[0]:
        for arg in args:
            plugin = get_plugin(arg)
            if plugin:
                l = []
                for k in plugin._handlers_msg.values():
                    if hasattr(k, '__handler_type__') and \
                       k.__handler_type__ == 'command':
                        if isinstance(k.__command_head__, list):
                            l.append(
                                '(%s)' % unicode(
                                    '|'.join(k.__command_head__)
                                )
                            )
                        else:
                            l.append(unicode(k.__command_head__))
                bot.msg(
                    channel,
                    u'Available commands for %s: %s' % (
                        arg,
                        u", ".join(l)
                    )
                )
            else:
                bot.msg(channel, u'Plugin %s not found' % arg)
    elif len(args) > 1:
        plugin_name = args.pop(0)
        plugin = get_plugin(plugin_name)
        if plugin:
            for arg in args:
                found = False
                for command in plugin._handlers_msg.values():
                    if isinstance(command.__command_head__, list):
                        commandlist = command.__command_head__
                    else:
                        commandlist = [command.__command_head__]
                    if arg in commandlist:
                        helptxt = command.__doc__
                        if not helptxt:
                            helptxt = "No doc available"
                        bot.msg(
                            channel, unicode(helptxt)
                        )
                        found = True
                        break
                if not found:
                    bot.msg(
                        channel,
                        u'Command %s in plugin %s not found' % (
                            arg,
                            plugin_name
                        )
                    )
        else:
            bot.msg(channel, u'Plugin %s not found' % plugin_name)
    else:
        help(bot, user, channel, '!help helper help')
        help(bot, user, channel, '!help helper plugins')
        bot.msg(
            channel,
            'load|unload|reload - Load/unload/reload a plugin'
        )


@helper.command('plugins')
def plugins(bot, user, channel, msg):
    '''plugins - List available plugins'''
    args = msg.split()[1:]
    if len(args) == 0:
        keys = sorted(_plugins.keys())

        bot.msg(channel,
                'Plugins loaded: %s' %
                (' '.join(keys),))
    elif args[0] == "save":
        _factory.config.plugins = _plugins.keys()
        bot.msg(channel, 'Plugins saved')


