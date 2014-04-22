# -*- coding: utf-8 -*-

import urllib, os

#facile à installer, il suffit de faire easy_install BeautifulSoup4
from bs4 import BeautifulSoup

#import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse

import datetime

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

def now_iso():

    d = datetime.datetime.now()

    yyyy = '%d'%d.year
    mm_0 = '%d'%d.month
    mm = mm_0.zfill(2)

    dd_0 = '%d'%d.day
    dd = dd_0.zfill(2)

    res = '%s%s%s'%(yyyy, mm, dd)

    return res

def is_int(s):

    try:
        x = float(s)
        return int(x) == x
    except:
        return False

def strip_all_t_and_n(s):
    s2 = s.strip('\n')
    s3 = s2.strip('\t').strip('\n').strip('\t').strip('\n').strip('\t').strip('\n')
    s4 = s3.strip('\t').strip('\n').strip('\t')
    return s4

def indent(elem, level=0):

    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class Parser_1:
    # site n°1
    def __init__(self, criteria):
        self.criteria = criteria
        self.root_url = url_builder.root_url_1

        self.cache_d = {}
        self.read_all_from_cache()

    def read_all_from_cache(self):

        page_idx = 1

        cache_file = self.get_cache_file(page_idx)

        while(os.path.exists(cache_file)):

            an_list = self.read_from_cache(page_idx)

            self.cache_d[page_idx] = an_list

            page_idx += 1
            cache_file = self.get_cache_file(page_idx)

    def get_cache_file(self, idx_page=1):

        iso = now_iso()

        cache_file = 'cache/parser_%s_page_%d.xml'%(iso,idx_page)

        return cache_file

    def get_annonce_list_at_page(self, idx_page=1):

        if idx_page in self.cache_d:
            res = self.cache_d[idx_page]
            return res

        search_url = url_builder.build_url_site_1(self.criteria, idx_page)
        search_html = urllib.urlopen(search_url).read()

        print 'search_url', search_url

        annonce_list = self.parse_search_result_page(search_html)

        self.write_to_cache(idx_page, annonce_list)

        return annonce_list

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

    def write_to_cache(self, idx_page, annonce_list):

        self.cache_d[idx_page] = annonce_list

        cache_file = self.get_cache_file(idx_page)

        root = Element("annonce_list")

        key_list = ['short_title', 'full_url', 'price', 'nb_pics', 'full_title', 'description', 
                    'image_src_list', 'surface', 'type', 'nb_rooms']

        #main = doc.createElement("annonce_list")

        for ii, an in enumerate(annonce_list):

            annonce = SubElement(root, 'annonce')

            for key in key_list:

                value = getattr(an, key)

                if key == 'image_src_list':
                    value = '@'.join(value)
                elif type(value) is int:
                    value = '%d'%value

                vvv = SubElement(annonce, key)
                vvv.text = value

        indent(root)

        f = open(cache_file, "w")
        ElementTree(root).write(f)
        f.close()

    def read_from_cache(self, idx_page):

        print 'reading from cache', idx_page

        cache_file = self.get_cache_file(idx_page)

        f = open(cache_file, "r")
        tree = parse(f)
        annonce_list_root = tree.getroot()

        annonce_elem_list = annonce_list_root.getchildren()

        res = []

        for an_elem in annonce_elem_list:

            an = Obj()

            for attr in an_elem.getchildren():

                key = attr.tag
                value = attr.text

                if key == 'image_src_list':
                    value = attr.text.split('@')
                elif is_int(value):
                    value = int(value)

                setattr(an, key, value)

            res.append(an)

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
        res.full_title = strip_all_t_and_n(res.full_title)
    
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

        res.type = strip_all_t_and_n(li_list[0].string)
        res.nb_rooms = strip_all_t_and_n(li_list[1].string)
        res.surface = strip_all_t_and_n(li_list[2].string)

        print ['nb_rooms', res.nb_rooms]

        return res
    
    def parse_annonce_full(self, annonce_soup):
    
        res = self.parse_annonce_in_search_page(annonce_soup)
    
        detailed_res = self.parse_annonce_own_page(res.full_url)

        #puis on copie les attributs sur l'objet de résultat    
        res.full_title = detailed_res.full_title
        res.description = detailed_res.description
        res.image_src_list = detailed_res.image_src_list

        res.type = detailed_res.type
        res.nb_rooms = detailed_res.nb_rooms
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

def get_annonce_list_1(criteria, page_idx):
    #parsing pour le site 1
    ps = Parser_1(criteria)
    res = ps.get_annonce_list_at_page(page_idx)

    return res

if __name__ == '__main__':
    
    parse_result_list()

    #res = get_annonce_list_1('', 1)

