from bot import BotPlugin
import subprocess

git = BotPlugin()

def git_head(folder, branch='master'):
    m = subprocess.Popen('cd %s; git log %s --pretty=format:"%%h >>>%%s<<< [%%aN]" HEAD -n 1' \
                             % (folder, branch),
                         shell=True, stdout=subprocess.PIPE).stdout
    return m.read()

@git.startswith('!head')
def say_git_head(bot, user, channel, msg):
    # TODO: check if branch exists
    # TODO: cleanup

    sp = msg.split()
    branch = 'master'
    if len(sp)>1:
        repo = sp[1]
    else:
        repo = ''
    if len(sp)>2:
        branch = sp[2]

    if repo == 'entchen':
        m = git_head('/admin/verwaltung/repository/entchen.git/', 
                     branch)
    elif repo == 'voliere':
        m = git_head('/admin/verwaltung/repository/verwaltung.git/',
                     branch)
    elif repo == 'issues':
        m = git_head('/admin/verwaltung/repository/issues.git/', 
                     branch)
    else:
        m = 'give name of repo (i.e. entchen, voliere)'
    bot.msg(channel, m)

