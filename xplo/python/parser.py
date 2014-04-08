# -*- coding: utf-8 -*-

import urllib

#facile à installer, il suffit de faire easy_install BeautifulSoup4
from bs4 import BeautifulSoup

import url_builder.url_builder_do_not_commit as url_builder

class Obj:
    def __init__(self):
        pass

class Criteria_Description:
    def __init__(self):

        self.for_sale = True
        self.for_renting = False
        self.area_min = 35
        self.location = 'paris+13eme+75013'

    def get_transaction_type_1(self):
        if self.for_sale:
            res = 'vente'
        else:
            res = 'location'

        return res


class Parser_1:
    # site n°1
    def __init__(self, criteria):
        self.criteria = criteria
        self.root_url = url_builder.root_url_1

    def get_and_parse_results(self, n_pages=8):

        res = []

        for idx_page in range(1, n_pages+1):

            search_url = url_builder.build_url_site_1(self.criteria, idx_page)
            search_html = urllib.urlopen(search_url).read()

            print 'search_url', search_url
            #f = open('bli.html', 'w')
            #f.write(search_html)
            #f.close()

            annonce_list = self.parse_search_result_page(search_html)

            res.extend(annonce_list)

        return res

    def parse_annonce_in_search_page(self, annonce_soup):
        '''renvoie un objet avec les champs :
        short_title, full_url, price, nb_pics'''
    
        res = Obj()
        soup = annonce_soup
    
        h2_list = soup.find_all('div', 'bloc-item-header')
        assert len(h2_list) == 1

        a_list = h2_list[0].find_all('a')
        assert len(a_list) == 1
        a = a_list[0]
    
        res.short_title = a.string
        res.href = a['href']
    
        res.full_url = self.root_url + res.href
    
        price_label_l = soup.find_all('span', 'price-label')

        res.price = price_label_l[0].string.replace(u'\xa0', ' ')

        res.nb_pics_str = soup.find_all('span', 'photo-count')[0].string
        res.nb_pics = int(res.nb_pics_str.split(' ')[0])

        return res

    def parse_annonce_own_page(self, own_url):
        '''remplit les champs full_title, description, image_src_list,
        surface, type, nb_rooms'''
    
        res = Obj()

        f = urllib.urlopen(own_url)
        html = f.read()
        soup = BeautifulSoup(html)
        
        l = soup.find_all('div', id='bloc-vue-detail')
        assert len(l) == 1
        l2 = l[0].find_all('h1')
        if len(l2) != 1:
            print 'error', own_url
            raise Exception('error parsing 1')
    
        #1 : le titre
    
        res.full_title = l2[0].string.replace('\n', '').strip(' ').replace('  ', '')
        res.full_title = res.full_title.replace(u'\xa0', '')
    
        #2 : la description
    
        l = soup.find_all('div', id='detailDescriptionTxt')
        assert len(l) == 1
    
        l2 = l[0].find_all('p', 'tJustify')
        if len(l2) == 0:
            #f = open('bla.html', 'wb')
            #f.write(html)
            #f.close()
            raise Exception('error parsing 2')
    
        desc = ''
    
        for i in range(len(l2)):
            for x in l2[i].strings:
                y = x.replace(u'\n', u'')
                desc += y
    
        res.description = desc
    
        #3 : les liens vers les photos
    
        l = soup.find_all('div', id='detailSlideLinks')
        assert len(l) == 1
        l2 = l[0].find_all('img')
    
        res.image_src_list = [x['src'] for x in l2]

        #4 : surface, nombre de pièces, type

        bien = soup.find_all('div', 'bien')
        li_list = bien[0].find_all('li')

        assert len(li_list) == 3

        res.type = li_list[0].string
        res.nb_pieces = li_list[1].string
        res.surface = li_list[2].string
    
        return res
    
    def parse_annonce_full(self, annonce_soup):
    
        res = self.parse_annonce_in_search_page(annonce_soup)
    
        detailed_res = self.parse_annonce_own_page(res.full_url)

        #puis on copie les attributs sur l'objet de résultat    
        res.full_title = detailed_res.full_title
        res.description = detailed_res.description
        res.image_src_list = detailed_res.image_src_list

        res.type = detailed_res.type
        res.nb_pieces = detailed_res.nb_pieces
        res.surface = detailed_res.surface
    
        return res
    
    def parse_search_result_page(self, html):
    
        soup = BeautifulSoup(html)
        annonce_list = soup.find_all('div', class_='js-bloc-vue')
    
        res = []    
    
        for annonce in annonce_list:
            res_an = self.parse_annonce_full(annonce)
    
            res.append(res_an)
    
            #titre_annonce = '<a href="%s">%s</a>'%(res_an.full_url, res_an.full_title)
            #line = [titre_annonce, res_an.surface, res_an.price, res_an.description]
    
        return res

def get_annonce_list_1(criteria, n_pages):
    #parsing pour le site 1
    ps = Parser_1(criteria)
    res = ps.get_and_parse_results(n_pages)

    return res

if __name__ == '__main__':
    
    parse_result_list()

    #res = get_annonce_list_1('', 1)

