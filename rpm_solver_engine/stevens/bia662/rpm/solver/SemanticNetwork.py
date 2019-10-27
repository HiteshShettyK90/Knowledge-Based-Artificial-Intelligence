'''
Created on Oct 9, 2019

@author: hites
'''
#This network updates the state of attributes 
#of first node from second node passed to the constructor
from builtins import staticmethod
class SemanticNetwork(object):
    '''
    classdocs
    '''
    #all_objects_modified this is required when number of objects in A is less than B
    #in this case the solution can have more objects with similar individual objects
    encp_attr_keys={'inside':True,'above':True,'left-of':True,'right-of':True,'overlaps':True}
    directional_attr_keys={'angle':True}
    
    def __init__(self, node1,node2):
        '''
        Constructor
        '''
        #print("-Bulding Semantic Network")
        #update the state of the attribute in B and the transformation_type in B
        self.all_objects_same=False
        self.node1state=None
        self.updateObjectState(node1, node2)
        self.node1state=node1
    
    def updateObjectState(self,node1,node2):
        transformation_type='transformation_type'
        deleted='deleted'
        for obj_name in node1.objs:
            #if obj name is not in node2 mark node1 trasformation_type to deleted
                if obj_name not in node2.objs:
                    node2.objs[obj_name]=node1.objs[obj_name]
                    node1.objs[obj_name].transformation_type=deleted
                else:
                    #careful if X to X relation does not match between A and B
                    self.compareAndUpdateAttrState(node1.objs[obj_name],node2.objs[obj_name])
                    
    #compare and update the state of attribute in A based on B
    def compareAndUpdateAttrState(self,entity1,entity2):
        #nothing to update if entity2 is not present
        if entity2 is None:
            return 
        #updated all single value attribute
        #iterate through the list of obj2 attr and update obj1 attr state
        #update single value attr
        self.updateSingleValueAttr(entity1, entity2)
        self.updateMultiValueAttr(entity1,entity2)
        #later might have to check for shapes
        #might have to add additional attributes to mention caveats to some attributes
        
    def updateSingleValueAttr(self,entity1,entity2):
        new_key='added'
        for attr in entity2.dict_single_val_attr:
            #update if attr is in 
            #print(entity1.dict_single_val_attr)
            if attr in entity1.dict_single_val_attr:
                #update sate in entity1 attr
                entity1.dict_single_val_attr[attr]['state']=entity2.dict_single_val_attr[attr]['attr_value']
                entity1.dict_single_val_attr[attr][new_key]=False
            else:
                entity1.dict_single_val_attr[attr]={}
                entity1.dict_single_val_attr[attr]['attr_value']=""
                entity1.dict_single_val_attr[attr]['state']=entity2.dict_single_val_attr[attr]['attr_value']
                entity1.dict_single_val_attr[attr][new_key]=True
                
            #print(entity1.dict_single_val_attr)
            #print("updated end")
        
    def updateMultiValueAttr(self,entity1,entity2):
        new_key='added'
        
        directional=[]
        for attr in entity2.dict_multi_val_attr:
            #update if attr is in 
            #print(entity1.dict_single_val_attr)
            #if in encp_list
            if attr not in entity1.dict_multi_val_attr:
                if attr in self.encp_attr_keys:
                    directional.append(attr)
            
            if attr in entity1.dict_multi_val_attr:
                #update sate in entity1 attr
                entity1.dict_multi_val_attr[attr]['state']=entity2.dict_multi_val_attr[attr]['attr_value']
                entity1.dict_multi_val_attr[attr][new_key]=False
            else:
                entity1.dict_multi_val_attr[attr]={}
                entity1.dict_multi_val_attr[attr]['attr_value']=""
                entity1.dict_multi_val_attr[attr]['state']=entity2.dict_multi_val_attr[attr]['attr_value']
                entity1.dict_multi_val_attr[attr][new_key]=True
                    
                
            #print(entity1.dict_single_val_attr)
            
            #print("updated end")
            
    def ismultivalattr(self,attr_name):
        if attr_name in self.encp_attr_keys:
            return True
        else:
            return False
    
            