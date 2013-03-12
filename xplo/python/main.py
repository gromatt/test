
import parser

import html_builder

import os, urllib

result_path = os.path.join(os.path.split(__file__)[0], '..', 'html_result')


def main_generate_annonce_list_html():

    criteria = parser.Criteria_Description()

    annonce_list = parser.get_annonce_list_1(criteria, n_pages=1)

    print 'data parsed, generating'

    html = html_builder.make_annonce_list_html(annonce_list)

    #print 'html', html

    html_file = os.path.join(result_path, 'res.html')

    f = open(html_file, 'wb')
    f.write(html)
    f.close()

if __name__ == '__main__':

    main_generate_annonce_list_html()