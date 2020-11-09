#!/usr/bin/env python
# -*- coding: utf8 -*-
import json
import sys
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs
from libs.constants import DEFAULT_ENCODING,PREDEFINED_CLASSES
from libs.ustr import ustr

TXT_EXT = '.json'
ENCODE_METHOD = DEFAULT_ENCODING

class YOLOWriter:

    def __init__(self, foldername, filename, imgSize, Acce,UserInfo,databaseSrc='Unknown', localImgPath=None,):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.Acce=Acce
        self.UserInfo=UserInfo
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

        dic = {
            'FileInfo': {
                "FileName": self.filename,
                "Width": self.imgSize[1],
                "Height": self.imgSize[0],
                "Channel": self.imgSize[2] if len(self.imgSize) == 3 else 1,
            },
            "UserInfo": {
                "ID": self.UserInfo[0],
                "Gender": self.UserInfo[1],
                "Age": self.UserInfo[2],
            },
            "Accessory": {
                "Mask": self.Acce[0],
                "Glasses": self.Acce[0],
                "Cap": self.Acce[0],
            },
            "Annotation": 1,
            "ObjectInfo": {
                'KeyPoints': {
                    'Count': 0,
                    "Points": [0] * 140,
                },
                "BoundingBox": {
                    "Face":{
                        "isVisible":False,
                        "Position" : [0,0,0,0]
                    },
                    "Leye": {
                        "isVisible": False,
                        "Opened":False,
                        "Position": [0, 0, 0, 0]
                    },
                    "Reye": {
                        "isVisible": False,
                        "Opened":False,
                        "Position": [0, 0, 0, 0]
                    },
                    "Mouth": {
                        "isVisible": False,
                        "Opened":False,
                        "Position": [0, 0, 0, 0]
                    },
                    "Cigar": {
                        "isVisible": False,
                        "Position": [0, 0, 0, 0]
                    },
                    "Phone": {
                        "isVisible": False,
                        "Position": [0, 0, 0, 0]
                    }
                },

            }

        }


        return dic

    def addBndBox(self, xmin, ymin, xmax, ymax, name, difficult):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        bndbox['difficult'] = difficult
        self.boxlist.append(bndbox)

    def appendObjects(self):
        for each_object in self.boxlist:
            if each_object['name'] in PREDEFINED_CLASSES:
                sp=each_object['name'].split("_")
                if len(sp)==2:
                    self.dic["ObjectInfo"]["BoundingBox"][sp[0]]={
                        "isVisible":True,
                        "Opened": True if sp[1]=="OPEN" else False,
                        "Position": [int(each_object['xmin']),int(each_object['ymin']),int(each_object['xmax']),int(each_object['ymax'])]
                    }

                else:
                    self.dic["ObjectInfo"]["BoundingBox"][each_object['name']] = {
                        "isVisible": True,
                        "Position": [int(each_object['xmin']), int(each_object['ymin']), int(each_object['xmax']),
                                     int(each_object['ymax'])]
                    }


    def save(self, targetFile=None):

        
        self.dic = self.genDict()
        self.appendObjects()
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                self.filename + TXT_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)

        out_file.write(json.dumps(self.dic, indent=4, sort_keys=False, ensure_ascii=False))
        out_file.close()



class YoloReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.json_dic={}
        self.accessory={}
        self.filepath = filepath


        self.verified = False
        # try:
        self.parseJSON()
        # except:
            # pass

    def getShapes(self):
        return self.shapes

    def getDict(self):
        return self.json_dic

    def addShape(self, label, bndbox, difficult):
        xmin = int(float(bndbox[0]))
        ymin = int(float(bndbox[1]))
        xmax = int(float(bndbox[2]))
        ymax = int(float(bndbox[3]))
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, None, None, difficult))

    def parseJSON(self):
        assert self.filepath.endswith(TXT_EXT)

        f = codecs.open(self.filepath, encoding="utf-8")
        dic=json.loads(f.read())
        f.close()

        self.json_dic=dic

        for object_name in dic["ObjectInfo"]["BoundingBox"].keys():
            if dic["ObjectInfo"]["BoundingBox"][object_name]["isVisible"]:
                label=object_name
                bndbox=dic["ObjectInfo"]["BoundingBox"][object_name]["Position"]
                difficult = False
                self.addShape(label, bndbox, difficult)


        return True
