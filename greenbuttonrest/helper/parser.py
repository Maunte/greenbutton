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
        entry["links"] = []
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
                    entry["links"].append(topentry.attrib["href"])
        return entry

    def auth_entry(self, entry):
        entrydict = {"links": []}
        for child in entry:
            entrytag = self.rm_namespace(child.tag)
            if entrytag == "title":
                entrydict["title"] = child.text
            elif entrytag == "id":
                entrydict["uuid"] = child.text
            elif entrytag == "link":
                entrydict["links"].append(child.attrib["href"])
            elif entrytag == "content":
                content = []
                for items in child:
                    for item in items:
                        itemdict = {}
                        itemtag = self.rm_namespace(item.tag)
                        if itemtag == "publishedPeriod" or itemtag == "authorizedPeriod":
                            itemdict[itemtag] = []
                            for time in item:
                                itemdict[itemtag].append({self.rm_namespace(time.tag): item.text})
                        else:
                            itemdict[itemtag] = item.text
                        content.append(itemdict)
                entrydict["content"] = content
            else:
                entrydict[entrytag] = child.text
        return entrydict

    def app_info(self):
        self.data["method"] = "app_info"
        self.data["entries"] = []
        self.data["links"] = []
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
                    self.data["links"].append(child.attrib["href"])
        return self.data

    def app_info_by_id(self):
        self.data["method"] = "app_info_by_id"
        self.data["entry"] = self.entry_read(self.root)
        return self.data

    def auth(self):
        self.data["method"] = "auth"
        self.data["entries"] = []
        self.data["links"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entrydict = self.auth_entry(child)
                self.data["entries"].append(entrydict)
            else:
                if tag != "link":
                    self.data[tag] = child.text
                else:
                    self.data["links"].append(child.attrib["href"])
        print(self.data)
        return self.data

    def auth_id(self):
        self.data["method"] = "auth_id"
        self.data["entry"] = self.auth_entry(self.root)
        return self.data

    def batch(self):
        self.data["method"] = "batch"
        self.data["links"] = []
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
                    self.data["links"].append(child.attrib["href"])
        return self.data

    def batch_retail(self):
        self.data["method"] = "batch_retail"
        self.data["entries"] = []
        self.data["links"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "link":
                self.data["links"].append(child.attrib["href"])
            elif tag == "entry":
                entrydict = {}
                entrydict["links"] = []
                for entry in child:
                    entrytag = self.rm_namespace(entry.tag)
                    if entrytag == "title":
                        entrydict["title"] = entry.text
                    elif entrytag == "id":
                        entrydict["uuid"] = self.rm_urn(entry.text)
                    elif entrytag == "link":
                        entrydict["links"].append(entry.attrib["href"])
                    elif entrytag == "content":
                        content = []
                        for subcontent in entry:
                            subcondict = {}
                            subcontag = self.rm_namespace(subcontent.tag)
                            if subcontent.iter() is not None:
                                subcondict[subcontag] = []
                                for item in subcontent:
                                    itemtag = self.rm_namespace(item.tag)
                                    if item.iter() is not None:
                                        itemdict = {}
                                        for subitem in item:
                                            itemdict[self.rm_namespace(subitem.tag)] = subitem.text
                                        if len(itemdict) > 0:
                                            subcondict[subcontag].append(itemdict)
                                        else:
                                            pass
                                    else:
                                        subcondict[subcontag].append({itemtag: item.text})
                            else:
                                content.append({subcontag: "N/A"})
                            content.append(subcondict)
                        entrydict["content"] = content
                    self.data["entries"].append(entrydict)
            else:
                self.data[tag] = child.text
        print(self.data)
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
            elif tag == "link":
                self.data["links"].append(child.attrib["href"])
            else:
                self.data[tag] = child.text

        else:
            pass
        return self.data

    def electric_power_usage(self):
        self.data["method"] = "epower_usage"
        self.data["entries"] = []
        self.data["links"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entrydict = {"links": []}
                for entry in child:
                    entrytag = self.rm_namespace(entry.tag)
                    if entrytag == "title":
                        entrydict["title"] = entry.text
                    elif entrytag == "id":
                        entrydict["uuid"] = self.rm_urn(entry.text)
                    elif entrytag == "link":
                        entrydict["links"].append(entry.attrib["href"])
                    elif entrytag == "content":
                        entrydict["content"] = []
                        for cont in entry:
                            for subcontent in cont:
                                subdict = {}
                                items = []
                                subtag = self.rm_namespace(subcontent.tag)
                                for item in subcontent:
                                    items.append({self.rm_namespace(item.tag): item.text})
                                if len(items) == 0:
                                    subdict[subtag] = subcontent.text
                                else:
                                    subdict[subtag] = items
                                entrydict["content"].append(subdict)
                    else:
                        entrydict[entrytag] = entry.text
                self.data["entries"].append(entrydict)
            elif tag == "link":
                self.data["links"].append(child.attrib["href"])
            else:
                self.data[tag] = child.text
        return self.data

    def electric_power_usage_summary(self):
        self.data["method"] = "epower_usage_summary"
        self.data["links"] = []
        for entry in self.root:
            entrytag = self.rm_namespace(entry.tag)
            if entrytag == "title":
                self.data["title"] = entry.text
            elif entrytag == "id":
                self.data["uuid"] = self.rm_urn(entry.text)
            elif entrytag == "link":
                self.data["links"].append(entry.attrib["href"])
            elif entrytag == "content":
                self.data["content"] = []
                for cont in entry:
                    for subcontent in cont:
                        subdict = {}
                        items = []
                        subtag = self.rm_namespace(subcontent.tag)
                        for item in subcontent:
                            items.append({self.rm_namespace(item.tag): item.text})
                        if len(items) == 0:
                            subdict[subtag] = subcontent.text
                        else:
                            subdict[subtag] = items
                        self.data["content"].append(subdict)
            else:
                self.data[entrytag] = entry.text
        print(self.data)
        return self.data

    def specific_interval(self):
        self.data["method"] = "specific_interval"
        self.data["links"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data[tag] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "link":
                self.data["links"].append(child.attrib["href"])
            elif tag == "content":
                self.data["content"] = []
                for block in child:
                    for items in block:
                        interval = {}
                        itemstag = self.rm_namespace(items.tag)
                        interval[itemstag] = {}
                        for item in items:
                            itemtag = self.rm_namespace(item.tag)
                            if itemtag == "timePeriod":
                                for time in item:
                                    interval[itemstag][self.rm_namespace(time.tag)] = time.text
                            else:
                                interval[itemstag][itemtag] = item.text
                        if interval is not None:
                            self.data["content"].append(interval)
                        else:
                            pass
            else:
                self.data[tag] = child.text
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
        self.data["links"] = []
        for child in self.root:
            tag = self.rm_namespace(child.tag)
            if tag == "title":
                self.data["title"] = child.text
            elif tag == "id":
                self.data["uuid"] = self.rm_urn(child.text)
            elif tag == "entry":
                entry = self.entry_read(child)
                self.data["entries"].append(entry)
            elif tag == "link":
                self.data["links"].append(child.attrib["href"])
            else:
                self.data[tag] = child.text
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
        print(self.data)
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
