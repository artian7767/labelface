#!/usr/bin/env python
# -*- coding: utf8 -*-
import json
import sys

import codecs
from libs.constants import DEFAULT_ENCODING,PREDEFINED_CLASSES
from libs.ustr import ustr


JSON_EXT = '.json'
ENCODE_METHOD = DEFAULT_ENCODING

class CustomJSONWriter:

    def __init__(self, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
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

        dic = {
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

                },

            }

        }


        return dic

    def addBndBox(self, xmin, ymin, xmax, ymax, name, difficult):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        bndbox['difficult'] = difficult
        self.boxlist.append(bndbox)

    def appendObjects(self, diction):
        for each_object in self.boxlist:
            if each_object['name'] in PREDEFINED_CLASSES:
                diction["ObjectInfo"]["BoundingBox"][each_object["name"]]["isVisible"]=True
                diction["ObjectInfo"]["BoundingBox"][each_object["name"]]["Position"]=[int(each_object['xmin']),int(each_object['ymin']),int(each_object['xmax']),int(each_object['ymax'])]
        return diction

    def save(self, targetFile=None):

        
        dic = self.genDict()
        dic=self.appendObjects(dic)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                self.filename + JSON_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)

        out_file.write(json.dumps(dic, indent=4, sort_keys=False, ensure_ascii=False))
        out_file.close()


class CustomJSONReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.json_dic={}
        self.accessory={}
        self.filepath = filepath
        self.verified = False
        try:
            self.parseJSON()
        except:
            pass

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
        assert self.filepath.endswith(JSON_EXT)

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
