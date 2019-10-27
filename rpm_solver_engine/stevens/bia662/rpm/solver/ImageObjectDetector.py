'''
Created on Oct 26, 2019

@author: hites
'''
import cv2
import numpy as np
import re

class ImageObjectDetector:
    '''
    classdocs
    '''
    def __init__(self, problem):
        '''
        Constructor
        '''
        #print(problem)
        self.solution = problem["solution"]
        print(self.solution)
        self.node_images={}
        self.entities={}
        self.nodes=dict()
        self.node_cx=0
        self.node_cy=0
        img_file_exp = "([A-C|1-6]).png$"
        fh="file handler"
        delete_key_list={'object_id':True}
        for img in problem["images"]:
            node=dict()
            node_exp = re.search(img_file_exp, img)
            node_name = node_exp.group(1)
            print("{}".format(node_name))
            self.detect(img,fh)
            #reset name in entity with object_id
            print("hitesh")
            updated_entites={}
            for shape in self.entities:
                self.setSize(shape,self.entities)
                object_shape=shape
                object_id=str(self.entities[shape]['object_id']).upper()
                updated_entites[object_id]=self.entities[shape]
                updated_entites[object_id]['shape']=object_shape

                #delete object Id once processed
                for attr_key in delete_key_list:
                    del updated_entites[object_id][attr_key]

            self.entities = updated_entites
            self.nodes[node_name]=updated_entites
            #print(img)


    def setSize(self,shape,entities):
        area_threshold_by_shape={'shape_4':12000,'shape_3':5000,'circle':12000}
        area_list=entities[shape]['area']
        if len(area_list) > 2:
            pass
            #decide later
        else:
            area = entities[shape]['area'][0]
            shape_without_counter = shape.split("@")[0]
            if shape_without_counter in area_threshold_by_shape:
                if area < area_threshold_by_shape[shape_without_counter]:
                    entities[shape]['size'] = 'small'
                else:
                    entities[shape]['size'] = 'large'
            else:
                if area < 5000:
                    entities[shape]['size'] = 'small'
                else:
                    entities[shape]['size'] = 'large'

        #delete area once it is processed
        print(entities[shape]['area'])
        del entities[shape]['area']

    def create_entity(self,entities,shape,counter,area,cnt):
        entities[shape] = dict()
        entities[shape]['count'] = 1
        entities[shape]['object_id'] = chr(counter)
        entities[shape]['area'] = [area]
        # set angle of rotation
        rect = cv2.minAreaRect(cnt)[2]
        #entities[shape]['angle'] = int(rect) + 45
        #entities[shape]['angle'] = int(rect)
        # find the centroid
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        eps = 50
        if cx < self.node_cx - eps:
            entities[shape]['left-of-center'] = True
        elif cx > self.node_cx - eps:
            entities[shape]['right-of-center'] = True
        else:
            entities[shape]['x-center'] = True

        if cy < self.node_cy - eps:
            entities[shape]['below-of-center'] = True
        elif cy > self.node_cy - eps:
            entities[shape]['above-of-center'] = True
        else:
            entities[shape]['y-center'] = True
        #default fill to yes and change it when there is similar area ratio
        #entities[shape]['fill'] = 'yes'

    def detect(self,fileName,fh):

        img_path=fileName
        img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
        _,threshold=cv2.threshold(img, 100, 255,cv2.THRESH_BINARY)
        contours,hierarchy=cv2.findContours(threshold,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # get the node centroid for detecting the sides
        M = cv2.moments(contours[0])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        self.node_cx=cx
        self.node_cy=cy

        entities=dict()
        counter=100
        for cnt in contours[1:]:
            # polygon must be closed
            #changed 0.01 to 0.08
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(img,[approx],0,(0,0,0),4)
            shape,sides,area = self.detectShape(img,cnt,approx)
            # we will have to detect change in side count with different arc length to determine if circles wrongly detected with other polygons
            circle_sides_threshold=12
            if sides > circle_sides_threshold:
                shape = "circle"

            if shape in entities:
                print("hitesh:{}".format(area / entities[shape]['area'][len(entities[shape]['area']) - 1]))
                if (len(entities[shape]['area']) > 2  and abs(area - entities[shape]['area'][len(entities[shape]['area'])-2]) < 50):
                    self.create_entity(entities, shape+"@"+str(counter), counter, area, cnt)
                    counter += 1
                else:
                    entities[shape]['count'] = entities[shape]['count'] + 1
                    entities[shape]['area'].append(area)
                    #entities[shape]['fill'] = 'no'
            else:
                self.create_entity(entities,shape,counter,area,cnt)
                counter +=1


            #box = cv2.boxPoints(rect)
            #box = np.int0(box)


            #print("shape:"+shape)
        #self.detectAttr(entities)
        print(entities)
        self.entities=entities


    def detectAttr(self,entities):
        # if shape count ==2 then add attribute fill
        for shape in entities:
            if entities[shape]['count'] == 1:
                entities[shape]['fill'] = 'yes'
            elif entities[shape]['count'] == 2:
                entities[shape]['fill'] = 'no'
            else:
                entities[shape]['fill'] = 'no'

    def detectShape(self,img,cnt,approx):
        sides = len(approx)
        # print(sides)
        cv2.fillPoly(img, pts=[cnt],color=(100 + (10 * sides % 155), 100 + (10 * sides % 155), 100 + (10 * sides % 155)))
        shape="shape_{}".format(sides)

        area = cv2.contourArea(cnt)

        #below for testing only
        #cv2.imshow("shapes",img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #only for testing ends
        return shape,sides,area

