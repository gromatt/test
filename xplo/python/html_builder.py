import os

encoding = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'

template_path = os.path.join(os.path.split(__file__)[0], '..', 'templates')

from genshi.template import TemplateLoader

loader = TemplateLoader([template_path])

def make_annonce_list_html(annonce_list):

	tmpl = loader.load('annonce_list.html')
	stream = tmpl.generate(annonce_list=annonce_list)
	return stream.render()