# coding=utf-8
import re

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


@issues.command('issues')
def search_issues(bot, user, channel, msg):
    """
    searches github.com for entchen's issues via api
    """
    if not msg:
        return

    if numberish(msg):
        number = extract_number(msg)
        issue = gh['repos']['anatidae']['entchen']['issues'][number]()
        url = issue['html_url']

        send_txt = "#{} at {} {}".format(number, url, issue['title'])
    else:
        query = "{} {} {}".format(msg, default_state, repo)
        issue_list = gh['search']['issues'](q=query, sort=sort, type=issue_type)

        urls = []
        for each_issue in issue_list['items']:
            each_url = each_issue['html_url']
            urls.append(each_url)

        send_txt = " ".join(urls)

    bot.msg(channel, send_txt)

