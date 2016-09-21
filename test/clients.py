import requests


class GreenButtonClient(object):
    def __init__(self, access_token, endpoint, *args, **kwargs):
        self.endpoint = endpoint
        self.headers = {"authorization": access_token, "cache-control": "no cache"}
        self.url = "https://services.greenbuttondata.org:443/DataCustodian" + endpoint
        self.args = args
        self.kwargs = kwargs
        self.params = ""

    def execute(self, *args, **kwargs):
        method_map = {
            "/espi/1_1/resource/ApplicationInformation": self.application_information,
            "/espi/1_1/resource/Authorization": self.authorization,
            "/espi/1_1/resource/IntervalBlock": self.interval_block,
            "/espi/1_1/resource/LocalTimeParameters": self.local_time_parameters,
            "/espi/1_1/resource/MeterReading": self.meter_reading,
            "/espi/1_1/resource/ReadingType": self.reading_type,
            "/espi/1_1/resource/ReadServiceStatus": self.read_service_status,
            "/espi/1_1/resource/UsagePoint": self.usage_point,
        }

        result = method_map[self.endpoint](*args, **kwargs)
        return result

    def set_param_string(self):
        i = 1
        if len(self.kwargs) == 0:
            self.params = ""
        else:
            for kwarg in self.kwargs:
                if len(self.kwargs) == 1:
                    self.params = "?" + kwarg + "=" + self.kwargs[kwarg]
                else:
                    if i == 1:
                        self.params = "?" + kwarg + "=" + self.kwargs[kwarg] + "&"
                    else:
                        self.params = self.params + kwarg + "=" + self.kwargs[kwarg]
                        if i != len(self.kwargs):
                            self.params += "&"
                i += 1

    def application_information(self, *args, **kwargs):
        print "GETing Application Information..."

        if len(self.args) == 1:
            self.url += "/" + self.args[0]
        elif len(self.args) > 1:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def authorization(self, *args, **kwargs):
        print "GETing Authorizations"

        if len(self.args) == 1:
            self.url += "/" + self.args[0]
        elif len(self.args) > 1:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def interval_block(self, *args, **kwargs):
        print "GETing Interval Block"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def local_time_parameters(self, *args, **kwargs):
        print "GETing Local Time Parameters"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def meter_reading(self, *args, **kwargs):
        print "GETing Meter Reading"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def reading_type(self, *args, **kwargs):
        print "GETing Reading Type"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def read_service_status(self, *args, **kwargs):
        print "GETing Read Service Status"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def usage_point(self, *args, **kwargs):
        print "GETing Usage Point"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text
