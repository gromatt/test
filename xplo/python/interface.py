# -*- coding: latin-1 -*-   

import parser

def is_int(s):

    try:
        x = float(s)
        return int(x) == x
    except:
        return False

class Condition:

    def __init__(self, attribute, condition_type, condition_argument):

        self.attribute = attribute
        self.condition_type = condition_type
        self.condition_argument = condition_argument

    def condition_applies(self, annonce):

        attribute_value = getattr(annonce, self.attribute)
        arg = self.condition_argument

        attribute_value = attribute_value.lower()
        arg = arg.lower()

        if self.condition_type == 'contains':
            if attribute_value.find(arg) != -1:
                return True
            else:
                return False
        elif self.condition_type == 'does_not_contain':
            if attribute_value.find(arg) == -1:
                return True
            else:
                return False
        else:
            raise Exception('blou')

def annonce_respects_all_conditions(an, condition_list):

    for cond in condition_list:
        if not cond.condition_applies(an):
            return False

    return True

class Filter:

    def __init__(self):

        self.condition_list = []
        self.nb_filtrered_l = []
        self.nb_filtrered_total = 0
        self.nb_filtered_computed = True
        self.is_detail_visible = True

    def add_condition(self, attribute, condition_type, condition_argument):

        t = condition_argument.split('@')

        for arg_i in t:
            c = Condition(attribute, condition_type, arg_i)

            n_conditions = len(self.condition_list)
            c.id = 'condition_%d'%(n_conditions+1)

            self.condition_list.append(c)

    def compute_filter_on_annonces(self, all_annonces):

        still_in = {}

        for an in all_annonces:
            still_in[an.id] = True

        for cond in self.condition_list:

            nb_filtered = 0

            for an in all_annonces:

                xx = cond.condition_applies(an)

                if not xx:
                    if still_in[an.id]:
                        nb_filtered += 1
                    still_in[an.id] = False

            self.nb_filtered_l.append(nb_filtered)

        self.nb_filtrered_total = sum(self.nb_filtered_l)

        self.nb_filtered_computed = True

        return still_in

class Interface: #c'est l'objet où vont être stockées toutes les données du serveur

    def __init__(self):

        self.filter_list = []  
        self.filter_d = {}      

        self.annonce_list = {}

        self.nb_filtered = []
        self.nb_filtered_computed = False

        self.annonce_list_respecting_all_conditions = {}

        self.criteria = parser.Criteria_Description()
        self.parser_1 = parser.Parser_1(self.criteria)

    def add_filter(self, filter_name):

        f = Filter()
        n = len(self.filter_list)

        f.id = 'filter_%d'%(n+1)

        self.filter_list.append(f)
        self.filter_d[f.id] = f

    def add_condition(self, filter_id, attribute, condition_type, condition_argument):

        f = self.filter_d[filter_id]

        f.add_condition(attribute, condition_type, condition_argument)

        self.refresh_condition_matrix()

    def get_annonces(self, page_idx=1):        

        ll = self.parser_1.get_annonce_list_at_page(page_idx)

        for ii, an in enumerate(ll):
            an.id = 'page_%d_idx_%d'%(page_idx, ii+1)

        self.annonce_list[page_idx] = ll

        self.nb_filtered_computed = False

        #for an in self.annonce_list:
            #print an.description

    def get_all_current_annonces(self):

        res = []

        for page_idx in self.annonce_list:

            res.extend(self.annonce_list[page_idx])

        return res

    def refresh_condition_matrix(self):

        self.condition_m = {}

        self.nb_filtered = []

        still_in = {}

        all_annonces = self.get_all_current_annonces()        

    def get_annonce_list_respecting_conditions(self, page_idx=0):
        
        self.refresh_condition_matrix()

        if page_idx != 0 and page_idx in self.annonce_list_respecting_all_conditions:
            return self.annonce_list_respecting_all_conditions[page_idx]
        else:
            res = []
            for ii, vv in self.annonce_list_respecting_all_conditions.iteritems():
                res.extend(vv)
            return res