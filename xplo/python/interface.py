# -*- coding: latin-1 -*-   

import parser

class Condition:

    def __init__(self, attribute, condition_type, condition_argument):

        self.attribute = attribute
        self.condition_type = condition_type
        self.condition_argument = condition_argument

    def condition_applies(self, annonce):

        attribute_value = getattr(annonce, self.attribute)
        arg = self.condition_argument

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
        self.annonce_list = []

        self.nb_filtered = []
        self.nb_filtered_computed = False

    def add_condition(self, attribute, condition_type, condition_argument):

        n_conditions = len(self.condition_list)

        c = Condition(attribute, condition_type, condition_argument)

        c.id = 'condition_%d'%(n_conditions+1)

        self.condition_list.append(c)

    def get_annonces(self):

        criteria = parser.Criteria_Description()

        self.annonce_list = parser.get_annonce_list_1(criteria, page_idx=1)

        for ii, an in enumerate(self.annonce_list):
            an.id = 'xplo_%d'%(ii+1)

        #for an in self.annonce_list:
            #print an.description

    def refresh_condition_matrix(self):

        self.condition_m = {}

        self.nb_filtered = []

        still_in = {}

        for an in self.annonce_list:
            still_in[an.id] = True

        for cond in self.condition_list:

            nb_filtered = 0

            for an in self.annonce_list:

                print 'an', an

                xx = cond.condition_applies(an)

                if not xx:
                    if still_in[an.id]:
                        nb_filtered += 1
                    still_in[an.id] = False

            self.nb_filtered.append(nb_filtered)

        self.annonce_list_respecting_all_conditions = [x for x in self.annonce_list if still_in[x.id]]

        self.nb_filtered_computed = True

    def get_annonce_list_respecting_conditions(self):
        
        self.refresh_condition_matrix()

        return self.annonce_list_respecting_all_conditions