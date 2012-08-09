class Config:
    plugins = ['chatter', 'date', 'git', 'sysinfo', 'alarm', 'gw', 'randomness']
    port = 6667
    ssl = False
    commandchars = "!" # values like "!." mean either "!" or "."
    separators = ",:; " # for "entchen, join #test"

class EntchenConfig(Config):
    nickname = 'entchen'
    server = '188.40.78.73'
    port = 6668
    ssl = True
    channels = ['#cl-study', '#admin']

class TestConfig(EntchenConfig):
    nickname = 'testchen'
    channels = ['#test', '#test2']

class CeciConfig(Config):
    nickname = 'ceci'
    server = 'ceci.dastier.net'
    channels = ['#ceci']
    plugins = ['sysinfo']
