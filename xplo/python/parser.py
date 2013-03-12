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

        self.on_sale = True
        self.for_renting = False
        self.area_min = 35
        self.location = 'paris+13eme+75013'



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

            annonce_list = self.parse_search_result_page(search_html)

            res.extend(annonce_list)

        return res

    def parse_annonce_in_search_page(self, annonce_soup):
        '''renvoie un objet avec les champs :
        short_title, surface, type, nb_rooms, full_url, price, nb_pics'''
    
        res = Obj()
        soup = annonce_soup
    
        def get_sub_str(loc_soup, key, class_name):
    
            l = loc_soup.find_all(key, class_name)
            assert len(l) == 1
    
            return l[0].string
            
        def get_info_bien(bien_soup):
    
            res.surface = get_sub_str(bien_soup, 'li', 'm2')
            res.type = get_sub_str(bien_soup, 'li', 'type')
            res.nb_rooms = get_sub_str(bien_soup, 'li', 'tn')        
    
        h2_list = soup.find_all('h2')
        assert len(h2_list) == 1
    
        a_list = h2_list[0].find_all('a')
        assert len(a_list) == 1
        a = a_list[0]
    
        res.short_title = a.string
        res.href = a['href']
    
        res.full_url = self.root_url + res.href
    
        total_list = soup.find_all('div', 'total')
        assert len(total_list) == 1
        a_list = total_list[0].find_all('a')
        assert len(a_list) == 1
    
        res.price = a_list[0].string.replace(u'\xa0', ' ')
    
        res.nb_pics_str = soup.find_all('div', 'sprEI legende')[0].string
        res.nb_pics = int(res.nb_pics_str.split(' ')[0])
    
        bien_soup_list = soup.find_all('div', 'bien')
        assert len(bien_soup_list) == 1
        get_info_bien(bien_soup_list[0])
    
        return res
    
    def parse_annonce_own_page(self, own_url):
        '''remplit les champs full_title, description, image_src_list'''
    
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
    
        return res
    
    def parse_annonce_full(self, annonce_soup):
    
        res = self.parse_annonce_in_search_page(annonce_soup)
    
        detailed_res = self.parse_annonce_own_page(res.full_url)

        #puis on copie les attributs sur l'objet de résultat    
        res.full_title = detailed_res.full_title
        res.description = detailed_res.description
        res.image_src_list = detailed_res.image_src_list
    
        return res
    
    def parse_search_result_page(self, html):
    
        soup = BeautifulSoup(html)
        annonce_list = soup.find_all('div', class_='bloc-vue-in')
    
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
