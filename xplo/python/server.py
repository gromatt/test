
import cherrypy

import html_builder

from interface import *

class HelloWorld:

    def __init__(self):
        
        self.itf = Interface()

    def index(self):

        res = html_builder.make_main()

        return res

    index.exposed = True

    def get_conditions_html(self):

        res = html_builder.make_conditions_html(itf=self.itf)

        #print 'conditions html'
        #print res
        return res

    get_conditions_html.exposed = True

    def get_add_condition_form(self):

        res = html_builder.make_add_condition_form()

        print 'res', res
        return res

    get_add_condition_form.exposed = True

    def add_condition(self, attribute, boolean_function, argument):

        pass

    add_condition.exposed = True


cherrypy.config.update({'server.socket_host': 'localhost',
                        'server.socket_port': 13502,
                       })

config =    {'/js/all.js':
                {
                    'tools.staticfile.on':True,
                    'tools.staticfile.filename':'/home/mat/git_root/test/xplo/js/all.js',
                },
            '/js/jquery.js':
                {
                    'tools.staticfile.on':True,
                    'tools.staticfile.filename':'/home/mat/git_root/test/xplo/js/jquery.js',
                },
            '/css/all.css':
                {
                    'tools.staticfile.on':True,
                    'tools.staticfile.filename':'/home/mat/git_root/test/xplo/css/all.css',
                },
            '/':
                {
                    'tools.caching.on':True
                }
            }

cherrypy.tree.mount(HelloWorld(), '/', config=config)
cherrypy.engine.start()
cherrypy.engine.block()