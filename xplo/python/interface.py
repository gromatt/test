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

class Interface: #c'est l'objet où vont être stockées toutes les données du serveur

    def __init__(self):
        
        self.condition_list = []
        self.annonce_list = {}

        self.nb_filtered = []
        self.nb_filtered_computed = False

        self.annonce_list_respecting_all_conditions = {}

        self.criteria = parser.Criteria_Description()
        self.parser_1 = parser.Parser_1(self.criteria)

    def add_condition(self, attribute, condition_type, condition_argument):

        t = condition_argument.split('@')

        for arg_i in t:
            c = Condition(attribute, condition_type, arg_i)

            n_conditions = len(self.condition_list)
            c.id = 'condition_%d'%(n_conditions+1)

            self.condition_list.append(c)

        self.nb_filtered_computed = False

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

            self.nb_filtered.append(nb_filtered)

        for page_idx in self.annonce_list:

            l = [x for x in self.annonce_list[page_idx] if still_in[x.id]]
            self.annonce_list_respecting_all_conditions[page_idx] = l

        self.nb_filtered_computed = True

    def get_annonce_list_respecting_conditions(self, page_idx=0):
        
        self.refresh_condition_matrix()

        if page_idx != 0 and page_idx in self.annonce_list_respecting_all_conditions:
            return self.annonce_list_respecting_all_conditions[page_idx]
        else:
            res = []
            for ii, vv in self.annonce_list_respecting_all_conditions.iteritems():
                res.extend(vv)
            return res