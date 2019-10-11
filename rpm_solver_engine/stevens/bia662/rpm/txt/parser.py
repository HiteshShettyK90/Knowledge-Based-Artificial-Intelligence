'''
Created on Oct 8, 2019

@author: hites
'''
import os 
from stevens.bia662.rpm.txt.basicproblem import BasicProblem2X1
if __name__ == '__main__':
    print("------------ Ravens Progressive Matrix ----------------")
    #extract problem list
    path = 'C:\\Users\\hites\\My Documents\\LiClipse Workspace\\rpm_solver_engine\\transformer\\in\\2x1 Basic Problems [TXT]'
    
    files = []
    #read list the problems to solve
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
    
    for f in files:
        
        #define extract objects from the input
        problem = BasicProblem2X1(f)
    #times = [match.group(1) for match in pattern.finditer(ifile.read())]
    pass    