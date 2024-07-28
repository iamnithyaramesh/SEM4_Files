from twisted.internet import reactor
from twisted.web import server, resource
import requests

class URLPage(resource.Resource):
    
    def render_GET(self, request):
        url = request.args["url".encode()][0].decode()
        content = self.fetch_url(url)
        return content

    def fetch_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            return b"Error: Failed to fetch URL"

site = server.Site(URLPage())

reactor.listenTCP(8108, site)
reactor.run()