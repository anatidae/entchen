# -*- coding: utf-8 -*-
from bot import BotPlugin
from os.path import expanduser, expandvars
import json

shorten = BotPlugin()


def get_google_api_key(fn='~/.config/.google-api-key'):
    """ Reads the google api key from a file.
    Put only the key inside the file. Nothing else.
    Get your own api key from https://code.google.com/apis/console
    """
    fn = expandvars(expanduser(fn))
    try:
        f = open(fn)
        key = f.read().strip()
        f.close()
    except:
        key = False
    return key


def shortenit(longurl):
    """ shorten the longurl using google shortener

    adds http:// if missing.
    for https you have to add it yourself before calling this function.
    reads the google api key using the get_google_api_key function

    return json object if successfull; False otherwise.
    """
    key = get_google_api_key()
    if not key:
        return False

    import urllib2
    url = 'https://www.googleapis.com/urlshortener/v1/url'
    if not longurl.startswith('http'):
        longurl = 'http://%s' % longurl
    post = {'longUrl': longurl,
            'key': key}

    req = urllib2.Request(url, json.dumps(post))
    req.add_header('Content-Type', 'application/json')
    r = urllib2.urlopen(req)
    response = r.read()
    return json.loads(response)


@shorten.command('shorten')
def shortencmd(bot, user, channel, msg):
    r = shortenit(msg)
    if r:
        if 'id' in r:
            m = 'Shortend %s to %s' % (r.get('longUrl'), r.get('id'))
            # :( twisted: exceptions.TypeError: Data must not be unicode
            bot.msg(channel, str(m))
            return
    m = 'usage: !shorten <url>'
    bot.msg(channel, m)
