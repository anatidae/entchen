class Config:
    plugins = ['chatter', 'date', 'alarm', 'randomness', 'birthday', 'sysinfo',
        'shorten', 'regex', 'helper', 'channel']
    port = 6667
    ssl = False
    commandchars = "!"   # values like "!." mean either "!" or "."
    separators = ",:; "  # for "entchen, join #test"


class EntchenConfig(Config):
    nickname = 'entchen'
    server = '188.40.78.73'
    port = 6668
    ssl = True
    storage = 'entchen.data'
    channels = ['#cl-study', '#admin']


class EntchenConfigFreenode(Config):
    # don't load all plugins on freenode, until we have some kind of acl
    plugins = ['chatter', 'date', 'alarm', 'randomness', 'birthday']
    nickname = 'kindchen'
    server = 'chat.freenode.net'
    storage = 'kindchen.data'
    port = 6697
    ssl = True
    channels = ['#kinder']


class TestConfig(EntchenConfig):
    nickname = 'testchen'
    channels = ['#test', '#test2']
    storage = 'test.data'


class CeciConfig(Config):
    nickname = 'ceci'
    server = 'ceci.dastier.net'
    storage = 'ceci.data'
    channels = ['#test']
    plugins = ['test']
