import os
import stevens.bia662.rpm.solver.txtparser as txtparser
from stevens.bia662.rpm.solver.ImageObjectDetector import ImageObjectDetector


def print_nodes_to_file(entities,file,solution):
    file_head=""
    with open(solution,"r") as in_file:
        file_head = in_file.read()
    with open(file,"+w") as out_file:
        out_file.writelines(file_head)
        for node_name in entities:
            out_file.write("\n"+node_name)
            for shape in entities[node_name]:
                out_file.write("\n\t" + shape)
                for attr in entities[node_name][shape]:
                    out_file.write("\n\t\t" + attr+":{}".format(entities[node_name][shape][attr]))


path = '..\\..\\..\\..\\transformer\\in\\2x1 Basic Problems [RAW]'
out_path = '..\\..\\..\\..\\transformer\\out'
files = []
# read list the problems to solve
problems={}
output_file=""
for r, d, f in os.walk(path):
    solution=""
    img_list=[]
    problem = {"solution": "", "images": []}
    for file in f:
        #solution
        if file.endswith(".txt"):
            solution =r+"\\"+file
            #create the directory if does not exists
            output_file = out_path+"\\"+file
        elif file.endswith(".png"):
            img_path=r+"\\"+file
            img_list.append(img_path)

    problem["solution"]=solution
    problem["images"]=img_list
    detector=ImageObjectDetector(problem)
    print(detector.nodes)

    print("################### done processing image ################")
    if len(output_file) > 0:
        print(output_file)
        print_nodes_to_file(detector.nodes, output_file,solution)


    print("################### Done writing to solution file ################")
    txtparser.solve()

