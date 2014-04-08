import os

encoding = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'

template_path = os.path.join(os.path.split(__file__)[0], '..', 'templates')

from genshi.template import TemplateLoader

loader = TemplateLoader([template_path])

def make_annonce_list_html(annonce_list):

	tmpl = loader.load('annonce_list.html')
	stream = tmpl.generate(annonce_list=annonce_list)
	return stream.render()

def make_conditions_html(itf):

	stream = loader.load('conditions.html').generate(itf=itf)
	return stream.render()

def make_add_condition_form():

	stream = loader.load('form_add_condition.html').generate()
	return stream.render()

def make_main():

	stream = loader.load('main.html').generate()
	return stream.render()