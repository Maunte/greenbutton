import json, re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring
from xmljson import BadgerFish
from collections import OrderedDict
from json import dumps


class ParseXml(object):
    def __init__(self, xml):
        self.xml = xml

    def parse(self):
        print("Parsing XML Response: ")

        root = ET.fromstring(self.xml)
        content = root.iter(tag="{http://www.w3.org/2005/Atom}content")
        for child in content:
            for item in child:
                print(item.tag, item.attrib, item.text)
        for child in root:
            if child.tag == "{http://www.w3.org/2005/Atom}entry":
                for group in child:
                    if group.tag == "{http://www.w3.org/2005/Atom}content":
                        for set in group:
                            for item in set:
                                print(item.tag, item.attrib, item.text)

    def tojson(self):
        print("Converting XML to JSON")
        bf = BadgerFish(dict_type=OrderedDict)
        myjson = json.loads(dumps(bf.data(fromstring(self.xml))))
        for key, value in myjson.items():
            print(key)

    def __str__(self):
        return self.xml
