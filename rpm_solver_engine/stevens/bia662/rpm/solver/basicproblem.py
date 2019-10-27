'''
Created on Oct 8, 2019

@author: hites
'''
import copy
import re
from stevens.bia662.rpm.solver.Node import Node
from stevens.bia662.rpm.solver.SemanticNetwork import SemanticNetwork
from stevens.bia662.rpm.solver.Tester import Tester

class BasicProblem2X1(object):
    '''
    classdocs
    '''
    problem_type_exp="2x1BasicProblem(\d+).txt"
    problem_name=""
    matrix_size=""
    solution=""
    named_matrix={}

    def __init__(self, file_name):
        '''
        Constructor
        '''
        p_exp = re.search(self.problem_type_exp, file_name)
        print("#################Parsing problem {} ##############".format(p_exp.group(1)))
        with open(file_name) as file:
            data = file.read()
            self.parse_problem(data)
            try:
                pass
                #self.parse_problem(data)
            except Exception as e:
                print("Error testing solution:".format(e))
            
            
    
    def parse_problem(self,data):
        
        #parse input data
        problem_exp = "((^.+\n)(.+\n)(.+\n)((.+(\n)?)+))"
        problem = re.search(problem_exp, data)
        self.problem_name=problem.group(2)
        self.matrix_size=problem.group(3)
        self.solution=problem.group(4)
        self.named_matrix=dict()
        print("Expected Solution:{}".format(self.solution))
        cells= problem.group(5)
        node_exp = "(\n?([A-Z|0-9])((\n\W([A-Z])(\n\W\W.*)+)+))"
        for match in re.finditer(node_exp, cells):
            node = Node(match.group(2),match.group(3))
            self.named_matrix[str(match.group(2))]  = node  
        semantic_network1=SemanticNetwork(self.named_matrix['A'],self.named_matrix['B'])
        c_copy = copy.copy(self.named_matrix['C'])
        for i in range(1,7):
            semantic_network3=SemanticNetwork(c_copy,self.named_matrix[str(i)])
            Tester.compareNetwork(semantic_network1,semantic_network3,i)