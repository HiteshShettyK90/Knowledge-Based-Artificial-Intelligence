'''
Created on Oct 9, 2019

@author: hites
'''
#compares node 1 with node 2
#This returns the state as match or not between two generated node networks

class Tester:
    '''
    classdocs
    '''
    ignore_attr_list={}
    encp_attr_keys={'inside':True,'above':True,'left-of':True,'right-of':True,'overlaps':True}
    directional_attr_keys={}
    def __init__(self):
        '''
        Constructor
        '''
        
        self.is_match=0
        self.transistion_count_miss = 0
        self.matched_solutions=[]  
             
    @staticmethod          
    def compareNetwork(network1,network2,solution):
        
        #print(network1.node1state.name)
        #print(network2.node1state.name)
        #for now assume Z in A relates to Z in B
        #compare for each object in second network compare to first network
        #when names are assumed to be same
        unmatch_total_count=0
        a_unmatched_obj=[]
        a_deleted_objects=[]
        for obj in network2.node1state.objs:
            #compare between obj
            if obj not in network1.node1state.objs:
                a_unmatched_obj.append(obj)
        for obj in network2.node1state.objs:
            #compare between obj
            if obj in network1.node1state.objs:
                intermideate_count=0
                if network1.node1state.objs[obj].transformation_type == "deleted":
                    if network2.node1state.objs[obj].transformation_type != "deleted":
                        unmatch_total_count+=1
                        #print("conflict:{}".format(obj))
                    else:
                        #for reference
                        a_deleted_objects.append(obj)
                        #continue when both are deleted
                        continue
                else:
                    
                    count = Tester.compareattr(network2.node1state.objs[obj],network1.node1state.objs[obj])
                    if count > 0:
                        intermideate_count+=1
                
                if intermideate_count > 0 and len(a_unmatched_obj) > 0:
                        found_match=False
                        for obj_name in a_unmatched_obj:
                            count = Tester.compareattr(network2.node1state.objs[obj_name],network1.node1state.objs[obj])
            
                            if count == 0:
                                found_match=True
                        if not found_match:
                            unmatch_total_count+=1
                elif intermideate_count > 0:
                    print("count.{}".format(unmatch_total_count))
                    unmatch_total_count+=1    
                    
                        
                    ##map multiple
        
        print("-------------------------------total Count:{} for solution {}".format(unmatch_total_count,solution))
        #print("Unmatched objects:{}".format(a_unmatched_obj))
        if unmatch_total_count == 0:
            #print("Testing Solution:{}".format(solution))
            print("Matched with solution:{}".format(solution))
            
    #obj2 corresponds to obj from C and obj 1 is from A    
    @staticmethod
    def compareattr(entity2,entity1):
        
        #compare individual attributes in obj2 and obj1
        #print(entity2.dict_single_val_attr)
        #if entity1.transformation_type == "deleted" and entity1.transformation_type == entity2.transformation_type:
            #print("-------------------------entity2 tt:{}".format(entity2.transformation_type))
        #    return 0
        
        cmp_count = Tester.comparesinglevalattr(entity2,entity1)
        if cmp_count == 0:
            cmp_count = Tester.comparemultivalattr(entity2,entity1)
        #print("compare count:{}".format(cmp_count))
        return cmp_count
    
    @staticmethod
    def comparesinglevalattr(entity2,entity1):
        scalar_attr={'angle':True}
        #compare individual attributes in obj2 and obj1
        #print(entity2.dict_single_val_attr)
        c_unchanged_attr={}
        a_unchanged_attr={}
        c_changed_attr={}
        a_changed_attr={}
        #print("State Transformation of C->Solution solution:")
        #print(entity2.dict_single_val_attr)
        #print("Trasformation state of A->B solution:")
        #print(entity1.dict_single_val_attr)
        c_scalar_diff={}
        a_scalar_diff={}
        for attr in entity2.dict_single_val_attr:
            #print("Entity2:{},{}".format(entity2.dict_single_val_attr[attr]['state'],entity2.dict_single_val_attr[attr]['attr_value']))
            if entity2.dict_single_val_attr[attr]['state'] == entity2.dict_single_val_attr[attr]['attr_value']:
                c_unchanged_attr[attr]=True
            else:
                if attr in scalar_attr:
                    state_val=entity2.dict_single_val_attr[attr]['state']
                    if state_val == '':
                        state_val='0'
                    ini_val= entity2.dict_single_val_attr[attr]['attr_value']
                    if ini_val == '':
                        ini_val='0'
                    c_scalar_diff[attr]=int(state_val) - int(ini_val)
                    if c_scalar_diff[attr] == 0:
                        c_unchanged_attr[attr]=True
                    else:
                        c_changed_attr[attr]=True
                else:
                    c_changed_attr[attr]=entity2.dict_single_val_attr[attr]['state']
            #Test in A if there was a transition
        for attr in entity2.dict_single_val_attr:
            #print("Entity1:{},{}".format(entity1.dict_single_val_attr[attr]['state'],entity1.dict_single_val_attr[attr]['attr_value']))
            if attr not in entity1.dict_single_val_attr:
                a_changed_attr[attr]=True
            else:
                #Hitesh---print(entity1.dict_single_val_attr[attr])
                if entity1.dict_single_val_attr[attr]['state'] == entity1.dict_single_val_attr[attr]['attr_value']:
                    a_unchanged_attr[attr]=True
                else:
                    if attr in scalar_attr:
                        state_val=entity1.dict_single_val_attr[attr]['state']
                        if state_val == '':
                            state_val ='0'
                        ini_val= entity1.dict_single_val_attr[attr]['attr_value']
                        if ini_val == '':
                            ini_val='0'
                        a_scalar_diff[attr]=int(state_val) - int(ini_val)
                        if a_scalar_diff[attr] == 0:
                            a_unchanged_attr[attr]=True
                        else:
                            a_changed_attr[attr]=True
                    else:
                        a_changed_attr[attr]=entity1.dict_single_val_attr[attr]['state']
                    
        
        for attr in c_unchanged_attr:
            if attr in a_unchanged_attr:
                a_unchanged_attr.pop(attr)
        
        for attr in c_changed_attr:
            if attr in a_changed_attr:
                #scalar check the difference, if the diff is same then that could be a match else not
                if attr in scalar_attr:
                    if attr in a_scalar_diff and attr in c_scalar_diff and c_scalar_diff[attr] == a_scalar_diff[attr]:
                        a_changed_attr.pop(attr)
                elif a_changed_attr[attr] == c_changed_attr[attr]:
                    a_changed_attr.pop(attr)
                    
        
        
                    
                #transitions in both C and A should be same
                #is there transition in C
        #print("s changed:{}".format(a_changed_attr))
        #print("s unchanged:{}".format(a_unchanged_attr))
        return len(a_changed_attr)+len(a_unchanged_attr)
    
    @staticmethod
    def comparemultivalattr(entity2,entity1):
        
        #compare individual attributes in obj2 and obj1
        #print(entity2.dict_single_val_attr)
        c_unchanged_attr={}
        a_unchanged_attr={}
        c_changed_attr={}
        a_changed_attr={}
        #print("State Transformation of C->Solution solution:")
        #print(entity2.dict_single_val_attr)
        #print("Trasformation state of A->B solution:")
        #print(entity1.dict_single_val_attr)
        #print("ENtity 2:",format(entity2.dict_multi_val_attr))
        #print("Entity1:".format(entity1.dict_multi_val_attr))
        #print(entity1.dict_multi_val_attr)
        for attr in entity2.dict_multi_val_attr:
            #print("Entity2:{},{}".format(entity2.dict_single_val_attr[attr]['state'],entity2.dict_single_val_attr[attr]['attr_value']))
            if attr not in entity1.dict_multi_val_attr:
                a_changed_attr[attr]=True
            else:
                state_list = entity2.dict_multi_val_attr[attr]['state']
                #print(state_list)
                state_list= state_list.split(',')
                ent_list = entity2.dict_multi_val_attr[attr]['attr_value']
                ent_list=ent_list.split(',')
                insec_list=[]
                #print(state_list)
                for ele in state_list:
                    if ele in ent_list:
                        insec_list.append(ele)
                #print(insec_list)
                
                if(len(insec_list) is not len(state_list)):
                    c_changed_attr[attr]=True
                else:
                    c_unchanged_attr[attr]=True
                    
                #Test in A if there was a transition
                #print("++++")
                #print(entity2.dict_multi_val_attr)
                #print(entity1.dict_multi_val_attr)
        for attr in entity2.dict_multi_val_attr:
            #print("Entity1:{},{}".format(entity1.dict_single_val_attr[attr]['state'],entity1.dict_single_val_attr[attr]['attr_value']))
            if attr not in entity1.dict_multi_val_attr:
                #A changed by adding more attributes in C
                a_changed_attr[attr]=True
            else:
                state_list = sorted(entity1.dict_multi_val_attr[attr]['state'].split(','))
                #if state_list is not None:
                #    state_list=state_list.sort()
                ent_list = sorted(entity1.dict_multi_val_attr[attr]['attr_value'].split(','))
                #if ent_list is not None:
                #    ent_list=ent_list.sort()
                #print(state_list)
                #print(ent_list)
                insec_list=[]
                #print(state_list)
                for ele in state_list:
                    if ele in ent_list:
                        insec_list.append(ele)
                #print(insec_list)
                
                if(len(insec_list) is not len(state_list)):
                    a_changed_attr[attr]=True
                else:
                    a_unchanged_attr[attr]=True
       
        for attr in c_unchanged_attr:
            if attr in a_unchanged_attr:
                a_unchanged_attr.pop(attr)
        
        for attr in c_changed_attr:
            if attr in a_changed_attr:
                if a_changed_attr[attr] == c_changed_attr[attr]:
                    a_changed_attr.pop(attr)
           
                #transitions in both C and A should be same
                #is there transition in C
        #print("changed:{} for {}".format(a_changed_attr,entity1.name))
        #print("unchanged:{} for {}".format(a_unchanged_attr,entity1.name))
        return len(a_changed_attr)+len(a_unchanged_attr)      
            
        