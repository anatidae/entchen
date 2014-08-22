from twisted.web.resource import Resource
from bot import BotPlugin

class HelloPage(Resource):

    def render_GET(self, request):
        return 'Hello World'

helloweb = BotPlugin()

@helloweb.init
def init(bot):
    if bot.webresource is None:
        print "Webserver isn't available!"
        return

    bot.webresource.putChild("hello", HelloPage())
