import xml.etree.ElementTree as ET


class Parser(object):
    def __init__(self, xml):
        self.xml_text = xml
        self.data = {}
        self.root = ET.fromstring(self.xml_text)

    def parser(self):
        data = self.method_select(self.root)
        return(data)

    def root_type(self, root):
        return self.rm_namespace(root.tag)

    def method_select(self, root):
        tag = self.root_type(root)
        if tag == "feed":
            data = self.feed_parse()
        elif tag == "entry":
            data = self.entry_parse(root)
        elif tag == "content":
            data = self.content_parse(root)
        else:
            data = {}
        return data

    def key_test(self, root, key):
        try:
            for child in root:
                childtag = self.rm_namespace(child.tag)
                if childtag == key:
                    return True
                else:
                    pass
        except AttributeError:
            if key in root:
                return True
            else:
                pass
        return False

    def create_header(self, root):
        header = {"links": []}
        for child in root:
            childtag = self.rm_namespace(child.tag)
            if childtag == "title":
                header["title"] = child.text
            elif childtag == "id":
                header["uuid"] = self.rm_urn(child.text)
            elif childtag == "link":
                header["links"].append(child.attrib["href"])
            elif childtag == "entry":
                if "entries" not in header:
                    header["entries"] = []
                else:
                    pass
            elif childtag == "content":
                if "content" not in header:
                    header["content"] = []
                else:
                    pass
            else:
                header[childtag] = child.text
        return header

    def feed_parse(self):
        feed_dict = self.create_header(self.root)
        for child in self.root:
            childtag = self.rm_namespace(child.tag)
            if childtag == "entry":
                feed_dict["entries"].append(self.entry_parse(child))
            else:
                pass
        return feed_dict

    def entry_parse(self, entry):
        entry_dict = self.create_header(entry)
        if "entries" in entry_dict:
            del entry_dict["entries"]
        entry_dict["content"] = []
        for child in entry:
            childtag = self.rm_namespace(child.tag)
            if childtag == "content":
                entry_dict["content"] = self.content_parse(child)
            else:
                pass
        return entry_dict

    def content_parse(self, contents):
        contents_list = []
        for content in contents:
            content_dict = {}
            contenttag = self.rm_namespace(content.tag)
            if contenttag == "published":
                content_dict["published"] = contenttag.text
            elif contenttag == "updated":
                content_dict["updated"] = contenttag.text
            else:
                content_dict[contenttag] = []
                for resource in content:
                    content_dict[contenttag].append(self.resource_parse(resource))
            contents_list.append(content_dict)
        return contents_list

    def resource_parse(self, resource):
        resourcetag = self.rm_namespace(resource.tag)
        if resource.text.strip() != "":
            return {resourcetag: resource.text, "var_type": "str"}
        else:
            resources = []
            for subitem in resource:
                resources.append(self.resource_parse(subitem))
            return {resourcetag: resources, "var_type": "list"}

    def rm_namespace(self, name):
        if "{http://www.w3.org/2005/Atom}" in name:
            new_name = name.replace("{http://www.w3.org/2005/Atom}", "")
        elif "{http://naesb.org/espi}" in name:
            new_name = name.replace("{http://naesb.org/espi}", "")
        else:
            new_name = name
        return new_name

    def rm_urn(self, uuid):
        if "urn:uuid:" in uuid:
            return uuid.replace("urn:uuid:", "")
        else:
            return uuid