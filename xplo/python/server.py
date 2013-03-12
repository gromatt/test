
import cherrypy, urllib

from main import UrlBuilder
import make_html, parse_expl

url_builder = UrlBuilder()

class HelloWorld:

    def index(self, i):

    	print 'i', [i]
    	url = url_builder.build_url(int(i))
    	search_html = urllib.urlopen(url)
    	an_list = parse_expl.parse_html_search_result(search_html)
    	html = make_html.make_result_list_html(an_list)
    	return html

        return "Hello world!"
    index.exposed = True

    def get_results(self):

    	pass

obj = HelloWorld()

#cherrypy.config.update('config_cherrypy')

cherrypy.quickstart(obj, '/', 'config_cherrypy')