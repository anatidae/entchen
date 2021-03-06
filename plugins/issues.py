# coding=utf-8
import re

from twisted.web.resource import Resource

from bot import BotPlugin
# noinspection PyUnresolvedReferences
from zipa import api_github_com as gh


issues = BotPlugin()

regex = re.compile(r'^#?(?P<n>\d+)$')


def numberish(message_string):
    """
    Checks if the given string could represent a issue ID for github

    :param message_string: string to check
    :return: bool
    """
    assert message_string

    potential_number = message_string.split()[0]

    if regex.match(potential_number):
        return True

    return False


def extract_number(string):
    """
    Returns the number of a numberish string

    :param string: a string that was declared numberish
    :type string: str
    :return: extracted number as string
    :rtype: str
    """
    matches = regex.match(string)
    number = matches.group('n')

    return number


default_state = "state:open"
repo = "repo:anatidae/entchen"
sort = "updated"
issue_type = "issue"

class GitHubAPICallback(Resource):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    def render_GET(self, request):
        self.bot.msg("#kinder", unicode(request.args))
        return repr(request.args)

@issues.init
def init_issues(factory):
    if factory.webresource is None:
        print "Webserver isn't available!"
        return

    print "Issues Plugin init"
    if hasattr(factory, "bot"):
        factory.webresource.putChild("github", GitHubAPICallback(factory.bot))
    else:
        print "No bot instance...."

@issues.command('issues')
def search_issues(bot, user, channel, msg):
    """
    searches github.com for entchen's issues via api
    """
    if not msg:
        return

    query = "{} {} {}".format(msg, default_state, repo)
    issue_list = gh['search']['issues'](q=query, sort=sort, type=issue_type)

    if int(issue_list['total_count']) > 0:
        urls = []
        for each_issue in issue_list['items']:
            each_url = each_issue['html_url']
            urls.append(each_url)

        send_txt = " ".join(urls)
    else:
        send_txt = "No issues for '{}' found".format(msg)

    bot.msg(channel, send_txt)

@issues.command('issue')
def show_issue(bot, user, channel, msg):
    """
    shows link to given issue number if it is still open
    """
    if not msg:
        return

    if numberish(msg):
        number = extract_number(msg)
        try:
            issue = gh['repos']['anatidae']['entchen']['issues'][number]()
            url = issue['html_url']

            send_txt = "#{} at {} {}".format(number, url, issue['title'])
        except KeyError:
            send_txt = "#{} not found or not open"

        bot.msg(channel, send_txt)
