'''
Created on Oct 9, 2019

@author: hites
'''
import re
from stevens.bia662.rpm.solver.Entity import Entity
class Node:
    '''
    classdocs
    '''

    def __init__(self, name,obj_list_str):
        '''
        Constructor
        '''
        #print("Node Name:{}".format(name))
        #print(obj_list_str)
        self.objs={}
        self.name=name
        entity_exp="(\W([A-Z])((\n\W\W.*)+))"
        for match in re.finditer(entity_exp, obj_list_str):
            #print(match.group(2))
            #print(match.group(3))
            obj_name=match.group(2)
            obj_rep=match.group(3)
            entity =Entity(obj_name,obj_rep)
            #print("Entity name:{}".format(entity.name))
            #print("Entity attributes:{}".format(entity.dict_single_val_attr))
            self.objs[obj_name]=entity