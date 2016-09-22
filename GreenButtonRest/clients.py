import requests


class GreenButtonClient(object):
    def __init__(self, access_token, endpoint, *args, **kwargs):
        self.endpoint = endpoint
        self.headers = {"Pragma": "no-cache", "authorization": access_token, "cache-control": "no cache"}
        self.url = "https://services.greenbuttondata.org:443/DataCustodian" + endpoint
        self.args = args
        self.kwargs = kwargs
        self.params = ""

    def execute(self, *args, **kwargs):
        method_map = {
            "/espi/1_1/resource/ApplicationInformation": self.application_information,
            "/espi/1_1/resource/Authorization": self.authorization,
            "/espi/1_1/resource/Batch/Bulk": self.batch_bulk,
            "/espi/1_1/resource/Batch/Subscription": self.batch_subscription,
            "/espi/1_1/resource/Batch/RetailCustomer": self.batch_retail_customer,
            "/espi/1_1/resource/Batch/Subscription/UsagePoint": self.batch_subscription_usage,
            "/espi/1_1/resource/Subscription/ElectricPowerQualitySummary": self.electric_power_quality_summary,
            "/espi/1_1/resource/Subscription/ElectricPowerQualitySummarybyId": self.electric_power_usage_summary_by_id,
            "/espi/1_1/resource/Subscription/ElectricPowerUsageSummary": self.electric_power_usage_summary,
            "/espi/1_1/resource/Subscription/ElectricPowerUsageSummarybyId": self.electric_power_usage_summary_by_id,
            "/espi/1_1/resource/IntervalBlock": self.interval_block,
            "/espi/1_1/resource/Subscription/IntervalBlock": self.all_interval_blocks,
            "/espi/1_1/resource/Subscription/IntervalBlockbyId": self.interval_block_by_id,
            "/espi/1_1/resource/LocalTimeParameters": self.local_time_parameters,
            "/espi/1_1/resource/MeterReading": self.meter_reading,
            "/espi/1_1/resource/Subscription/MeterReading": self.all_meter_readings_for_usage__point,
            "/espi/1_1/resource/Subscription/MeterReadingbyId": self.meter_reading_for_usage__point_by_id,
            "/espi/1_1/resource/ReadingType": self.reading_type,
            "/espi/1_1/resource/ReadServiceStatus": self.read_service_status,
            "/espi/1_1/resource/UsagePoint": self.usage_point,
            "/espi/1_1/resource/Subscription/UsagePoint": self.usage_points_by_subscription_id,
            "/espi/1_1/resource/Subscription/UsagePointbyId": self.usage_point_by_id,
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

    def application_information(self):
        print "GETing Application Information..."

        if len(self.args) == 1:
            self.url += "/" + self.args[0]
        elif len(self.args) > 1:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def authorization(self):
        print "GETing Authorizations"

        if len(self.args) == 1:
            self.url += "/" + self.args[0]
        elif len(self.args) > 1:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def batch_bulk(self):
        print "GETing Bulk Transfer from DataCustodian"

        if len(self.args) < 1:
            print "Bulk Id Required!"
        elif len(self.args) == 1:
            self.url += "/" + self.args[0]
        elif len(self.args) > 1:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def batch_subscription(self):
        print "GETing Subscription from DataCustodian"

        if len(self.args) < 1:
            print "Subscription Id Required!"
        elif len(self.args) == 1:
            self.url += "/" + self.args[0]
        elif len(self.args) > 1:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def batch_retail_customer(self):
        print "GETing UsagePoint for Retail Customer"

        if len(self.args) < 1:
            print "Customer Id Required!"
        elif len(self.args) == 1:
            self.url += "/" + self.args[0] + "/UsagePoint"
        elif len(self.args) > 1:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def batch_subscription_usage(self):
        print "GETing Authorizations"

        self.url = self.url[:-10]
        if len(self.args) < 2:
            print "Subscription and UsagePoint Ids Required!"
        elif len(self.args) == 2:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1]
        elif len(self.args) > 2:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def electric_power_quality_summary(self):
        print "GETing Electric Power Quality Summary"

        self.url = self.url[:-27]
        if len(self.args) < 2:
            print "Subscription and UsagePoint Ids Required!"
        elif len(self.args) == 2:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1] + "/ElectricPowerQualitySummary"
        elif len(self.args) > 2:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def electric_power_quality_summary_by_id(self):
        print "GETing Electric Power Quality Summary"

        self.url = self.url[:-31]
        if len(self.args) < 3:
            print "Subscription, UsagePoint, and Electric Power Quality Summary Ids Required!"
        elif len(self.args) == 3:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1] + "/ElectricPowerQualitySummary/" + self.args[2]
        elif len(self.args) > 3:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def electric_power_usage_summary(self):
        print "GETing Electric Power Usage Summary"

        self.url = self.url[:-25]
        if len(self.args) < 2:
            print "Subscription and UsagePoint Ids Required!"
        elif len(self.args) == 2:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1] + "/ElectricPowerUsageSummary"
        elif len(self.args) > 2:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def electric_power_usage_summary_by_id(self):
        print "GETing Electric Power Usage Summary"

        self.url = self.url[:-29]
        if len(self.args) < 3:
            print "Subscription, UsagePoint, and Electric Power Usage Summary Ids Required!"
        elif len(self.args) == 3:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1] + "/ElectricPowerUsageSummary/" + self.args[2]
        elif len(self.args) > 3:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def interval_block(self):
        print "GETing Interval Block"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def all_interval_blocks(self):
        print "GETing All Interval Blocks"

        self.url = self.url[:-13]
        if len(self.args) < 3:
            print "Subscription, UsagePoint, and Meter Reading Ids Required!"
        elif len(self.args) == 3:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1] + "/MeterReading/" + self.args[2] + "/IntervalBlock"
        elif len(self.args) > 3:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def interval_block_by_id(self):
        print "GETing Interval Block by Id"

        self.url = self.url[:-14]
        if len(self.args) < 4:
            print "Subscription, UsagePoint, Meter Reading, and Interval Block Ids Required!"
        elif len(self.args) == 4:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1] + "/MeterReading/" + self.args[2] + "/IntervalBlock/" + self.args[3]
        elif len(self.args) > 4:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def local_time_parameters(self):
        print "GETing Local Time Parameters"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def meter_reading(self):
        print "GETing Meter Reading"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def all_meter_readings_for_usage__point(self):
        print "GETing All Meter Readings for Usage Point"

        self.url = self.url[:-12]
        if len(self.args) < 2:
            print "Subscription and UsagePoint Ids Required!"
        elif len(self.args) == 2:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1] + "/MeterReading/"
        elif len(self.args) > 2:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def meter_reading_for_usage__point_by_id(self):
        print "GETing Meter Reading for Usage Point by Id"

        self.url = self.url[:-16]
        if len(self.args) < 3:
            print "Subscription and UsagePoint Ids Required!"
        elif len(self.args) == 3:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1] + "/MeterReading/" + self.args[2]
        elif len(self.args) > 3:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def reading_type(self):
        print "GETing Reading Type"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def read_service_status(self):
        print "GETing Read Service Status"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def usage_point(self):
        print "GETing Usage Point"
        self.set_param_string()
        self.url += self.params
        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def usage_points_by_subscription_id(self):
        print "GETing UsagePoints for Subscription Id"

        self.url = self.url[:-11]
        if len(self.args) < 1:
            print "Subscription Id Required!"
        elif len(self.args) == 1:
            self.url += "/" + self.args[0] + "/UsagePoint"
        elif len(self.args) > 1:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text

    def usage_point_by_id(self):
        print "GETing Usage Point by Id"

        self.url = self.url[:-10]
        if len(self.args) < 2:
            print "Subscription and UsagePoint Ids Required!"
        elif len(self.args) == 2:
            self.url = self.url + self.args[0] + "/UsagePoint/" + self.args[1]
        elif len(self.args) > 2:
            print "Too many *args"

        self.set_param_string()
        self.url += self.params

        response = requests.request("GET", self.url, headers=self.headers)
        return response.text