'''
Created on Oct 9, 2019

@author: hites
'''
import re 
class Entity:
    '''
    classdocs
    '''
    #encapsulation attr
    encp_attr_keys={'inside':True,'above':True,'left-of':True,'right-of':True,'overlaps':True}
    directional_attr_keys={}
    #encp_attr_keys={}
    #single valued scalar
    scalar_sv_attr_keys={}
    
    def __init__(self, name,attr_list_str):
        '''
        Constructor
        '''
        #print(name)
        #print(attr_list_str)
        #transformation type can be unchanged
        self.transformation_type='unchanged'
        self.dict_single_val_attr={}
        self.dict_multi_val_attr={}
        #dict_scalar_val_attr={}
        self.dict_encp_attr={}
        self.dict_scalar_val_attr={}
        #print("debug:{}".format(self.dict_single_val_attr))
        self.name=name
        attr_expr="(\n\W\W(.*):(.*))"
        for match in re.finditer(attr_expr, attr_list_str):
            
            #print(match.group(3))
            #check attr val size after split
            attr_name=match.group(2).strip()
            attr_val=match.group(3).strip()
            #val_list=attr_val.split(',')
            #print(val_list)
            #print(attr_val)
            processed=False
            val_key="attr_value"
            state_key="state"
            if attr_name in self.encp_attr_keys:
                #need to iterate the list for inside and above
                self.dict_encp_attr[attr_name]={val_key:attr_val,state_key:""}
                processed=True
                
            elif attr_name in self.scalar_sv_attr_keys:
                self.dict_scalar_val_attr[attr_name]={val_key:attr_val,state_key:""}
                processed=True
                
            #Set all other attributes which are not processed
            if  self.ismultivalattr(attr_name):
                #print(attr_name)
                #print(val_list)
                self.dict_multi_val_attr[attr_name]={val_key:attr_val,state_key:""}   
            else:
                self.dict_single_val_attr[attr_name]={val_key:attr_val,state_key:""}
                
    def ismultivalattr(self,attr_name):
        if attr_name in self.encp_attr_keys or attr_name in self.directional_attr_keys:
            return True
        else:
            return False
            
                
                
                
    