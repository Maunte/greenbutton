import xml.etree.ElementTree as ET


class ParseXml(object):
    def __init__(self, xml):
        self.xml = xml

    def parse(self):
        print("Parsing XML Response: ")
        root = ET.fromstring(self.xml)
        for child in root:
            for item in child:
                if "id" in item.tag:
                    print(item.tag, item.text)

    def __str__(self):
        return self.xml

