import xml.etree.ElementTree as ET


class Parser(object):
    def __init__(self, xml):
        self.xml_text = xml
        self.data = {}
        self.root = ET.fromstring(self.xml_text)

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

    def entry_read(self, child):
        entry = {}
        for topentry in child:
            topentrytag = self.rm_namespace(topentry.tag)
            if topentrytag == "title":
                entry["title"] = topentry.text
            elif topentrytag == "id":
                entry["uuid"] = self.rm_urn(topentry.text)
            elif topentrytag == "content":
                for content in topentry:
                    for subcontent in content:
                        subcontenttag = self.rm_namespace(subcontent.tag)
                        try:
                            if subcontent.text.replace(" ", "") == "\n":
                                entry[subcontenttag] = []
                                for attr in subcontent:
                                    entry[subcontenttag].append((self.rm_namespace(attr.tag), attr.text))
                            else:
                                entry[subcontenttag] = subcontent.text
                        except AttributeError:
                            pass
            else:
                if topentrytag != "link":
                    self.data[topentrytag] = child.text
                else:
                    pass
        return entry

    def app_info(self):
        self.data["method"] = "app_info"
        self.data["entries"] = []
        if "feed" in self.root.tag:
            for child in self.root:
                tag = self.rm_namespace(child.tag)
                if tag == "title":
                    self.data["title"] = child.text
                elif tag == "id":
                    self.data["uuid"] = self.rm_urn(child.text)
                elif tag == "entry":
                    entry = self.entry_read(child)
                    self.data["entries"].append(entry)
                else:
                    if tag != "link":
                        self.data[tag] = child.text
                    else:
                        pass
        else:
            pass
        return self.data

    def app_info_by_id(self):
        self.data["method"] = "app_info_by_id"
        self.data["entry"] = self.entry_read(self.root)
        return self.data

    def auth(self):
        self.data["method"] = "auth"
        self.data["entries"] = []
        if "feed" in self.root.tag:
            for child in self.root:
                tag = self.rm_namespace(child.tag)
                if tag == "title":
                    self.data["title"] = child.text
                elif tag == "id":
                    self.data["uuid"] = self.rm_urn(child.text)
                elif tag == "entry":
                    entry = self.entry_read(child)
                    self.data["entries"].append(entry)
                else:
                    if tag != "link":
                        self.data[tag] = child.text
                    else:
                        pass
        else:
            pass
        return self.data

    def auth_id(self):
        self.data["method"] = "auth_id"
        self.data["entries"] = self.entry_read(self.root)
        return self.data

    def batch(self):
        self.data["method"] = "batch"
        if "feed" in self.root.tag:
            for child in self.root:
                tag = self.rm_namespace(child.tag)
                if tag == "title":
                    self.data["title"] = child.text
                elif tag == "id":
                    self.data["uuid"] = self.rm_urn(child.text)
                else:
                    if tag != "link":
                        self.data[tag] = child.text
                    else:
                        pass
        else:
            pass
        return self.data

    def batch_retail(self):
        self.data["method"] = "batch_retail"
        self.data["entries"] = []
        if "feed" in self.root.tag:
            for child in self.root:
                tag = self.rm_namespace(child.tag)
                if tag == "title":
                    self.data["title"] = child.text
                elif tag == "id":
                    self.data["uuid"] = self.rm_urn(child.text)
                elif tag == "entry":
                    entry = self.entry_read(child)
                    self.data["entries"].append(entry)
                else:
                    if tag != "link":
                        print(tag)
                        if child.text.replace(" ", "") == "\n":
                            self.data[tag] = []
                            for subchild in child:
                                self.data[tag].append((self.rm_namespace(subchild.tag), subchild.text))
                        else:
                            self.data[tag] = child.text
                    else:
                        pass
        else:
            pass
        return self.data

    def electric_power_quality_summary(self):
        self.data["method"] = "epower_quality_summary"
        self.data["entries"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entry = self.entry_read(child)
                self.data["entries"].append(entry)
            else:
                if tag != "link":
                    self.data[tag] = child.text
                else:
                    pass
        else:
            pass
        return self.data

    def electric_power_usage(self):
        self.data["method"] = "epower_usage"
        self.data["entries"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entry = self.entry_read(child)
                self.data["entries"].append(entry)
            else:
                if tag != "link":
                    self.data[tag] = child.text
                else:
                    pass
        else:
            pass
        return self.data

    def electric_power_usage_summary(self):
        self.data["method"] = "epower_usage_summary"
        self.data["entries"] = self.entry_read(self.root)
        return self.data

    def local_time(self):
        self.data["method"] = "local_time"
        self.data["entries"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entry = self.entry_read(child)
                self.data["entries"].append(entry)
            else:
                if tag != "link":
                    self.data[tag] = child.text
                else:
                    pass
        else:
            pass
        return self.data

    def local_time_id(self):
        self.data["method"] = "local_time_id"
        self.data["entries"] = self.entry_read(self.root)
        return self.data

    def meter_reading(self):
        self.data["method"] = "meter_reading"
        self.data["entries"] = []
        if "feed" in self.root.tag:
            for child in self.root:
                tag = self.rm_namespace(child.tag)
                if tag == "title":
                    self.data["title"] = child.text
                elif tag == "id":
                    self.data["uuid"] = self.rm_urn(child.text)
                elif tag == "entry":
                    entry = self.entry_read(child)
                    self.data["entries"].append(entry)
                else:
                    if tag != "link":
                        self.data[tag] = child.text
                    else:
                        pass
        else:
            pass
        return self.data

    def meter_reading_id(self):
        self.data["method"] = "meter_reading_id"
        self.data["entries"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entry = self.entry_read(child)
                self.data["entries"].append(entry)
            else:
                if tag != "link":
                    self.data[tag] = child.text
                else:
                    pass
        else:
            pass
        return self.data

    def reading_type(self):
        self.data["method"] = "reading_type"
        self.data["entries"] = []
        if "feed" in self.root.tag:
            for child in self.root:
                tag = self.rm_namespace(child.tag)
                if tag == "title":
                    self.data["title"] = child.text
                elif tag == "id":
                    self.data["uuid"] = self.rm_urn(child.text)
                elif tag == "entry":
                    entry = self.entry_read(child)
                    self.data["entries"].append(entry)
                else:
                    if tag != "link":
                        self.data[tag] = child.text
                    else:
                        pass
        else:
            pass
        return self.data

    def reading_type_by_id(self):
        self.data["method"] = "reading_type_by_id"
        self.data["entry"] = self.entry_read(self.root)
        return self.data

    def service_status(self):
        self.data["method"] = "service_status"
        self.data["title"] = "Service Status"
        for child in self.root:
            if "currentStatus" in child.tag:
                self.data["status"] = child.text
            else:
                self.data["status"] = "No Status Returned"
        return self.data

    def usagepoint(self):
        self.data["method"] = "usagepoint"
        self.data["entries"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entry = self.entry_read(child)
                self.data["entries"].append(entry)
            else:
                if tag != "link":
                    self.data[tag] = child.text
                else:
                    pass
        else:
            pass
        return self.data

    def usagepoint_by_id(self):
        self.data = self.entry_read(self.root)
        self.data["method"] = "usagepoint_by_id"
        return self.data

    def usagepoint_sub(self):
        self.data["method"] = "usagepoint_sub"
        self.data["entries"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entry = self.entry_read(child)
                self.data["entries"].append(entry)
            else:
                if tag != "link":
                    self.data[tag] = child.text
                else:
                    pass
        else:
            pass
        return self.data

    def usagepoint_sub_by_id(self):
        self.data = self.entry_read(self.root)
        self.data["method"] = "usagepoint_sub_by_id"
        print(self.data)
        return self.data
