import xml.etree.ElementTree as ET


class ParseXml(object):
    def __init__(self, xml):
        self.xml_text = xml

    def parse_entry(self, child):
        entry = {}
        for items in child:
            if items.tag == "{http://www.w3.org/2005/Atom}title":
                entry["title"] = items.text
            elif items.tag == "{http://www.w3.org/2005/Atom}content":
                for item in items:
                    for part in item:
                        part_key = part.tag.replace("{http://naesb.org/espi}", "")
                        entry[part_key] = part.text
            else:
                pass
        return entry

    def parse_root(self, root, data):
        entry_count = 1
        for child in root:
            if child.tag == "{http://www.w3.org/2005/Atom}title":
                data["title"] = child.text
            elif child.tag == "{http://www.w3.org/2005/Atom}entry":
                entry = self.parse_entry(child)
                data["entries"].append(entry)
                entry_count += 1
            else:
                pass
        return data

    def parse(self):
        print("Parsing XML Response: ")

        data = {}
        data["entries"] = []
        root = ET.fromstring(self.xml_text)
        if "feed" in root.tag:
            data = self.parse_root(root, data)
        elif "entry" in root.tag:
            entry = self.parse_entry(root)
            data["entries"].append(entry)
        else:
            print("Error: Problem with 'root' tag.")
            data = {}
        return data

