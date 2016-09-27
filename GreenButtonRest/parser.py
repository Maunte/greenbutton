import xml.etree.ElementTree as ET


class ParseXml(object):
    def __init__(self, xml):
        self.xml = xml

    def parse(self):
        root = ET.fromstring(self.xml)
        for child in root:
            print(root.attrib)

    def __str__(self):
        return self.xml

