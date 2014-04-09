
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

        #print 'res', res
        return res

    get_add_condition_form.exposed = True

    def add_condition(self, attribute, boolean_function, argument):

        self.itf.add_condition(attribute, boolean_function, argument)

    add_condition.exposed = True

    def get_annonce_list_html(self):

        print '########## in get_annonce_list_html'

        annonce_list = self.itf.get_annonce_list_respecting_conditions()

        res = html_builder.make_annonce_list_html(annonce_list)

        print 'res', res

        return res

    get_annonce_list_html.exposed = True

    def refresh_request(self):

        self.itf.make_request('')

        return 'ok'

    refresh_request.exposed = True

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
            '/css/annonce_list.css':
                {
                    'tools.staticfile.on':True,
                    'tools.staticfile.filename':'/home/mat/git_root/test/xplo/css/annonce_list.css',
                },
            '/':
                {
                    'tools.caching.on':False
                }
            }

cherrypy.tree.mount(HelloWorld(), '/', config=config)
cherrypy.engine.start()
cherrypy.engine.block()