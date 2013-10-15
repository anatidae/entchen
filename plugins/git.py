from bot import BotPlugin
import subprocess

git = BotPlugin()


def git_head(folder, branch='master'):
    m = subprocess.Popen('cd %s; git log %s --pretty=format:"%%h >>>%%s<<< [%%aN] -- %%ar" HEAD -n 1' \
                             % (folder, branch),
                         shell=True, stdout=subprocess.PIPE).stdout
    return m.read()


@git.command('botversion')
def say_git_version(bot, user, channel, msg):
    b = subprocess.Popen('git log --pretty=format:"%h -- %ar" HEAD -n 1',
                         shell=True, stdout=subprocess.PIPE).stdout
    m = b.read().strip()
    bot.msg(channel, m)


@git.command('head')
def say_git_head(bot, user, channel, msg):
    # TODO: check if branch exists
    # TODO: cleanup

    sp = msg.split()
    branch = 'master'
    if len(sp) > 0:
        repo = sp[0]
    else:
        repo = ''
    if len(sp) > 1:
        branch = sp[1]

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
        m = 'give name of repo (i.e. entchen, voliere) [optional name of branch]'
    bot.msg(channel, m)
