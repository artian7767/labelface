#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys

import codecs
from libs.constants import DEFAULT_ENCODING
from libs.ustr import ustr


JSON_EXT = '.json'
ENCODE_METHOD = DEFAULT_ENCODING

class CustomJSONWriter:

    def __init__(self, foldername, filename, imgSize,databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def genDict(self):
        """
            Return JSON root dict
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = {
            'FileInfo': {
                "FileName": self.filename,
                "Width": self.imgSize[1],
                "Height": self.imgSize[0],
                "Channel": self.imgSize[2] if len(self.imgSize) == 3 else 1,
            },
            # "UserInfo": {
            #     "ID": 0,
            #     "Gender": 0,
            #     "Age": 0,
            # },
            # "Accessory": {
            #     "Mask": False,
            #     "Glasses": False,
            #     "Cap": False
            # },
            "Annotation": 1,
            "Object_Info": {
                'KeyPoints': {
                    'Count': 0,
                    "Points": [0] * 140,
                },
                "BoundingBox": {
                    # "Face": {
                    #     "isVisible": True,
                    #     "Position": [int(face_left), int(face_up), int(face_right) + 1, int(face_down) + 1]
                    # },
                    # "L_Eye": {
                    #     "isVisible": True,
                    #     "Opened": False if situation.find("졸음재현") != -1 else True,
                    #     "Position": [int(le_left), int(le_up), int(le_right) + 1, int(le_down) + 1]
                    # },
                    # "R_Eye": {
                    #     "isVisible": True,
                    #     "Opened": False if situation.find("졸음재현") != -1 else True,
                    #     "Position": [int(re_left), int(re_up), int(re_right) + 1, int(re_down) + 1]
                    # },
                    # "Mouth": {
                    #     "isVisible": False if isMask == True else True,
                    #     "Opened": True if situation.find("하품") != -1 else False,
                    #     "Position": [int(m_left), int(m_up), int(m_right) + 1,
                    #                  int(m_down) + 1] if isMask == False else [0, 0, 0, 0]
                    # },
                    # "Cigar": {
                    #     "isVisible": isCigar,
                    #     "Position": [
                    #         [int(m_left) - 10, int(m_up) - 10, int(m_right) + 10, int(m_down) + 10]] if isCigar else [0,
                    #                                                                                                   0,
                    #                                                                                                   0,
                    #                                                                                                   0]
                    # },
                    # "Phone": {
                    #     "isVisible": isPhone,
                    #     "Position": [int(face_right) + 1, int(face_up), int(face_right) + 100,
                    #                  int(face_down)] if isPhone else [0, 0, 0, 0]
                    # },
                },

            }

        }
        # if self.verified:
        #     top.set('verified', 'yes')


        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, name, difficult):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        bndbox['difficult'] = difficult
        self.boxlist.append(bndbox)

    def appendObjects(self, dict):
        for each_object in self.boxlist:
            pass
            # object_item = SubElement(top, 'object')
            # name = SubElement(object_item, 'name')
            # name.text = ustr(each_object['name'])
            # pose = SubElement(object_item, 'pose')
            # pose.text = "Unspecified"
            # truncated = SubElement(object_item, 'truncated')
            # if int(float(each_object['ymax'])) == int(float(self.imgSize[0])) or (int(float(each_object['ymin']))== 1):
            #     truncated.text = "1" # max == height or min
            # elif (int(float(each_object['xmax']))==int(float(self.imgSize[1]))) or (int(float(each_object['xmin']))== 1):
            #     truncated.text = "1" # max == width or min
            # else:
            #     truncated.text = "0"
            # difficult = SubElement(object_item, 'difficult')
            # difficult.text = str( bool(each_object['difficult']) & 1 )
            # bndbox = SubElement(object_item, 'bndbox')
            # xmin = SubElement(bndbox, 'xmin')
            # xmin.text = str(each_object['xmin'])
            # ymin = SubElement(bndbox, 'ymin')
            # ymin.text = str(each_object['ymin'])
            # xmax = SubElement(bndbox, 'xmax')
            # xmax.text = str(each_object['xmax'])
            # ymax = SubElement(bndbox, 'ymax')
            # ymax.text = str(each_object['ymax'])


    def save(self, targetFile=None):

        
        # root = self.genXML()
        # self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                self.filename + JSON_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)

        # prettifyResult = self.prettify(root)
        # out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


class CustomJSONReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath
        self.verified = False
        try:
            self.parseJSON()
        except:
            pass

    def getShapes(self):
        return self.shapes

    def addShape(self, label, bndbox, difficult):
        xmin = int(float(bndbox.find('xmin').text))
        ymin = int(float(bndbox.find('ymin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymax = int(float(bndbox.find('ymax').text))
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, None, None, difficult))

    def parseJSON(self):
        assert self.filepath.endswith(JSON_EXT)
        # parser = etree.XMLParser(encoding=ENCODE_METHOD)
        # xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        # filename = xmltree.find('filename').text
        # try:
        #     verified = xmltree.attrib['verified']
        #     if verified == 'yes':
        #         self.verified = True
        # except KeyError:
        #     self.verified = False
        #
        # for object_iter in xmltree.findall('object'):
        #     bndbox = object_iter.find("bndbox")
        #     label = object_iter.find('name').text
        #     # Add chris
        #     difficult = False
        #     if object_iter.find('difficult') is not None:
        #         difficult = bool(int(object_iter.find('difficult').text))
        #     self.addShape(label, bndbox, difficult)
        return True
