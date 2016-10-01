# -*- coding: utf-8 -*-
import requests

from GreenButtonRest.exceptions import GreenException

"""Client for GreenButton RESTful APIs.

Usage::

  >>> from GreenButtonRest.clientV2 import GreenClient
  >>> gc = GreenClient()
  >>> execute = gc.execute("authorization")
  >>> print(execute)
  >>> print(gc.API_CALLS_MADE)
"""


class GreenClient:
    host = None
    token = None
    API_CALLS_MADE = 0
    API_LIMIT = None

    def __init__(self, api_limit=None):
        self.host = "https://services.greenbuttondata.org:443/DataCustodian/espi/1_1/resource"
        self.API_LIMIT = api_limit

    def execute(self, method, *args, **kwargs):
        result = None
        for i in range(0, 10):
            try:

                method_map = {
                    "application_information": self.get_application_info,
                    "authorization": self.get_authorization,
                    "batch_bulk": self.get_batch_bulk,
                    "batch_subscription": self.get_batch_subscription,
                    "batch_retail": self.get_batch_retail_customer,
                    "batch_subscription_usage": self.get_batch_subscription_usage,
                    "electric_power_summary_quality": self.get_electric_power_quality_summary,
                    "electric_power_summary_usage": self.get_electric_power_usage_summary,
                    "interval_block": self.get_interval_block,
                    "interval_block_subscription_meter_usage": self.get_subscription_meter_usage_interval,
                    "local_time_parameter": self.get_local_time_parameters,
                    "meter_reading": self.get_meter_reading,
                    "meter_reading_subscription_usage": self.get_subscription_usage_meter_reading,
                    "reading_type": self.get_reading_type,
                    "service_status": self.get_read_service_status,
                    "usage": self.get_usage_point,
                    "usage_by_subscription": self.get_usage_point_by_subscription,
                }
                result = method_map[method](*args, **kwargs)
                self.API_CALLS_MADE += 1
            except GreenException as e:
                # TODO: Identify authentication errors
                # TODO: Include handling response codes: 200, 400, 403
                if e.code in [601, 602]:
                    self.authenticate()
                    continue
                else:
                    raise Exception({'message': e.message, 'code': e.code})
            break
        return result

    # --------- GENERAL ---------
    def authenticate(self):
        """ Authenticate to get Access Token.

        :param clientId: Client ID to get bearer token
        :param clientSecret: Client Secret to get bearer token
        :return token: sets token
        """

        # TODO: Generate token here
        self.token = "Bearer 2a85f4bd-30db-4b7d-8f41-b046b0566cb3"

    def build_params(self, published_max=None, published_min=None, updated_max=None, updated_min=None,
                     max_results=None, start_index=None, depth=None):
        """ Helper function to build request header with optional parameters.

        :param published_max: (optional) The upper bound on the published date of the Application Information.
        :type published_max: date
        :param published_min: (optional) The lower bound on the published date of the Application Information.
        :type published_min: date
        :param updated_max: (optional) The upper bound on the updated date of the Application Information.
        :type updated_max: date
        :param updated_min: (optional) The lower bound on the updated date of the Application Information.
        :type updated_min: date
        :param max_results: (optional) The upper bound on the number of entries to be contained in a reply to this
            response.
        :type max_results: long
        :param start_index: (optional) The one based offset in the DataCustodian's collection of Application Information
            that should be transferred as the first entry of this request.
        :type start_index: long
        :param depth: (optional) The maximum number of entries to be transferred in the response to this request.
        :type depth: long
        :return: dict:headers
        :rtype: dict
        """

        self.authenticate()
        headers = {
            "authorization": self.token
        }

        # TODO: value validation
        if published_max is not None:
            headers["published-max"] = published_max
        if published_min is not None:
            headers["published-min"] = published_min
        if updated_max is not None:
            headers["updated-max"] = updated_max
        if updated_min is not None:
            headers["updated-min"] = updated_min
        if max_results is not None:
            headers["max-results"] = max_results
        if start_index is not None:
            headers["start-index"] = start_index
        if depth is not None:
            headers["depth"] = depth
        return headers

    # --------- APPLICATION INFORMATION ---------

    def get_application_info(self,
                             application_information_id=None,
                             published_max=None,
                             published_min=None,
                             updated_max=None,
                             updated_min=None,
                             max_results=None,
                             start_index=None,
                             depth=None):
        """ Gets all application information. If an id is provided, get single

        :param application_information_id: (optional) The Id of the Application Information to be retrieved.
        :type application_information_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        url_built = self.host + "/ApplicationInformation/"

        if application_information_id is not None:
            url_built += str(application_information_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- AUTHORIZATION ---------

    def get_authorization(self,
                          authorization_id=None,
                          published_max=None,
                          published_min=None,
                          updated_max=None,
                          updated_min=None,
                          max_results=None,
                          start_index=None,
                          depth=None):
        """ Gets authorization information. If an id is provided, get single

        :param authorization_id: (optional) The Id of the Authorization Information to be retrieved.
        :type authorization_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        built_url = self.host + "/Authorization"

        if authorization_id is not None:
            built_url += str(authorization_id)

        result = requests.get(url=built_url, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- BATCH ---------

    def get_batch_bulk(self,
                       bulk_id,
                       published_max=None,
                       published_min=None,
                       updated_max=None,
                       updated_min=None,
                       max_results=None,
                       start_index=None,
                       depth=None):
        """ Gets batch information.

        :param bulk_id: (required) The Bulk Id as specified in the OAuth2 SCOPE string.
        :type bulk_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        result = requests.get(url=self.host + "/Batch/Bulk/" + str(bulk_id), headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_batch_subscription(self,
                               subscription_id,
                               published_max=None,
                               published_min=None,
                               updated_max=None,
                               updated_min=None,
                               max_results=None,
                               start_index=None,
                               depth=None):
        """ Gets batch subscription by subscriptionId.

        :param subscription_id: (required) The Subscription's Id.
        :type subscription_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        result = requests.get(url=self.host + "/Batch/Subscription/" + str(subscription_id), headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_batch_retail_customer(self,
                                  retail_customer_id,
                                  published_max=None,
                                  published_min=None,
                                  updated_max=None,
                                  updated_min=None,
                                  max_results=None,
                                  start_index=None,
                                  depth=None):
        """ Gets batch retail customer usage.

        :param retail_customer_id: (required) The Retail Customer's Id.
        :type retail_customer_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        result = requests.get(url=self.host + "/Batch/RetailCustomer/" + str(retail_customer_id) + "/UsagePoint",
                              headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_batch_subscription_usage(self,
                                     subscription_id,
                                     usage_point_id,
                                     published_max=None,
                                     published_min=None,
                                     updated_max=None,
                                     updated_min=None,
                                     max_results=None,
                                     start_index=None,
                                     depth=None):
        """ Gets batch information.

        :param subscription_id: (required) The Subscription's Id.
        :type subscription_id: str
        :param usage_point_id: (required) The UsagePoint's Id.
        :type usage_point_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        result = requests.get(
            url=self.host + "/Batch/Subscription/" + str(subscription_id) + "/UsagePoint/" + str(usage_point_id),
            headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- ELECTRIC POWER QUALITY SUMMARY ---------

    def get_electric_power_quality_summary(self,
                                           subscription_id,
                                           usage_point_id,
                                           electric_power_quality_summary_id=None,
                                           published_max=None,
                                           published_min=None,
                                           updated_max=None,
                                           updated_min=None,
                                           max_results=None,
                                           start_index=None,
                                           depth=None):
        """ Gets all electric power quality summaries. If an id is provided, get single

        :param subscription_id: (required) The Subscription's Id.
        :type subscription_id: str
        :param usage_point_id: (required) Id of the UsagePoint the Electric Power Quality Summary references.
        :type usage_point_id: str
        :param electric_power_quality_summary_id: (optional) Id of the Electric Power Quality Summary to be retrieved.
        :type electric_power_quality_summary_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        built_url = self.host + "/Subscription/" + str(subscription_id) + "/UsagePoint/" + str(
            usage_point_id) + "/ElectricPowerQualitySummary/"

        if electric_power_quality_summary_id is not None:
            built_url += built_url + str(electric_power_quality_summary_id)

        result = requests.get(url=built_url, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- ELECTRIC POWER USAGE SUMMARY ---------

    def get_electric_power_usage_summary(self,
                                         subscription_id,
                                         usage_point_id,
                                         electric_power_usage_summary_id=None,
                                         published_max=None,
                                         published_min=None,
                                         updated_max=None,
                                         updated_min=None,
                                         max_results=None,
                                         start_index=None,
                                         depth=None):
        """ Gets all electric power usage summary. If an id is provided, get single

        :param subscription_id: (required) The Subscription's Id.
        :type subscription_id: str
        :param usage_point_id: (required) Id of the UsagePoint the Electric Power Quality Summary references.
        :type usage_point_id: str
        :param electric_power_usage_summary_id: (optional) Id of the Electric Power Quality Summary to be retrieved.
        :type electric_power_usage_summary_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        built_url = self.host + "/Subscription/" + str(subscription_id) + "/UsagePoint/" + str(
            usage_point_id) + "/ElectricPowerUsageSummary/"

        if electric_power_usage_summary_id is not None:
            built_url += str(electric_power_usage_summary_id)

        result = requests.get(url=built_url, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- INTERVAL BLOCK ---------

    def get_interval_block(self,
                           interval_block_id=None,
                           published_max=None,
                           published_min=None,
                           updated_max=None,
                           updated_min=None,
                           max_results=None,
                           start_index=None,
                           depth=None):
        """ Gets all interval blocks. If an intervalBlockId is included, get single

        :param interval_block_id: (optional) Id of the Interval Block to be retrieved.
        :type interval_block_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)
        url_built = self.host + "/IntervalBlock/"

        if interval_block_id is not None:
            url_built += str(interval_block_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_subscription_meter_usage_interval(self,
                                              subscription_id,
                                              usage_point_id,
                                              meter_reading_id,
                                              interval_block_id=None,
                                              published_max=None,
                                              published_min=None,
                                              updated_max=None,
                                              updated_min=None,
                                              max_results=None,
                                              start_index=None,
                                              depth=None):

        """ Gets all interval blocks for usage and subscription and meter. If an intervalBlockId is included, get single

        :param subscription_id: (required) Id of the Retail Customer the Interval Block references.
        :type subscription_id: str
        :param usage_point_id: (required) Id of the UsagePoint the Interval Block references.
        :type usage_point_id: str
        :param meter_reading_id: (required) Id of the MeterReading the Interval Block references.
        :type meter_reading_id: str
        :param interval_block_id: (optional) Id of the Interval Block to be retrieved.
        :type interval_block_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)
        url_built = self.host + "/Subscription/" + str(subscription_id) + "/UsagePoint/" + str(
            usage_point_id) + "/MeterReading/" + str(meter_reading_id) + "/IntervalBlock/"

        if interval_block_id is not None:
            url_built += str(interval_block_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- LOCAL TIME PARAMETERS ---------

    def get_local_time_parameters(self,
                                  local_time_parameter_id=None,
                                  published_max=None,
                                  published_min=None,
                                  updated_max=None,
                                  updated_min=None,
                                  max_results=None,
                                  start_index=None,
                                  depth=None):

        """ Gets all local time parameters. If an id is included, get single

        :param local_time_parameter_id: (optional) Id of the Interval Block to be retrieved.
        :type local_time_parameter_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)
        url_built = self.host + "/LocalTimeParameters/"

        if local_time_parameter_id is not None:
            url_built += str(local_time_parameter_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- METER READING ---------

    def get_meter_reading(self,
                          meter_reading_id=None,
                          published_max=None,
                          published_min=None,
                          updated_max=None,
                          updated_min=None,
                          max_results=None,
                          start_index=None,
                          depth=None):

        """ Gets all meter readings. If an id is included, get single

        :param meter_reading_id: (optional) Id of the Meter Reading.
        :type meter_reading_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)
        url_built = self.host + "/MeterReading/"

        if meter_reading_id is not None:
            url_built += str(meter_reading_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_subscription_usage_meter_reading(self,
                                             subscription_id,
                                             usage_id,
                                             meter_reading_id=None,
                                             published_max=None,
                                             published_min=None,
                                             updated_max=None,
                                             updated_min=None,
                                             max_results=None,
                                             start_index=None,
                                             depth=None):

        """ Gets all meter readings usage readings. If an id is included, get single

        :param subscription_id: (required) Id of the Subscription associated with the Usage Point containing the Meter
            Reading.
        :type subscription_id: str
        :param usage_id: (required) Id of the UsagePoint the Meter Reading references.
        :type usage_id: str
        :param meter_reading_id: (optional) Id of the Meter Reading.
        :type meter_reading_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)
        url_built = self.host + "/Subscription/" + str(subscription_id) + "/UsagePoint/" + str(
            usage_id) + "/MeterReading/"

        if meter_reading_id is not None:
            url_built += str(meter_reading_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- READING TYPE ---------

    def get_reading_type(self,
                         reading_type_id=None,
                         published_max=None,
                         published_min=None,
                         updated_max=None,
                         updated_min=None,
                         max_results=None,
                         start_index=None,
                         depth=None):
        """ Gets all reading types. If an id is included, get single

        :param reading_type_id: (optional) ID of the Reading Type.
        :type reading_type_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)
        url_built = self.host + "/ReadingType/"

        if reading_type_id is not None:
            url_built += str(reading_type_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- SERVICE STATUS ---------

    def get_read_service_status(self):
        """ Gets service status.

        :return: xml result
        :rtype text/xsl
        """

        self.authenticate()

        headers = {
            "authorization": self.token
        }

        url_built = self.host + "/ReadServiceStatus"

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- USAGE POINT ---------

    def get_usage_point(self,
                        usage_point_id=None,
                        published_max=None,
                        published_min=None,
                        updated_max=None,
                        updated_min=None,
                        max_results=None,
                        start_index=None,
                        depth=None):
        """ Gets all usage points. If an id is included, get single

        :param usage_point_id: (optional) Id of the Usage Point.
        :type usage_point_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)
        url_built = self.host + "/UsagePoint/"

        if usage_point_id is not None:
            url_built += str(usage_point_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_usage_point_by_subscription(self,
                                        subscription_id,
                                        usage_point_id=None,
                                        published_max=None,
                                        published_min=None,
                                        updated_max=None,
                                        updated_min=None,
                                        max_results=None,
                                        start_index=None,
                                        depth=None):
        """ Gets all usage points by subscription. If an id is included, get single

        :param subscription_id: (required) The Subscription's Id.
        :type subscription_id: str
        :param usage_point_id: (optional) Id of the Usage Point.
        :type usage_point_id: str

        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)
        url_built = self.host + "/Subscription/" + str(subscription_id) + "/UsagePoint/"

        if usage_point_id is not None:
            url_built += str(usage_point_id)

        result = requests.get(url=url_built, headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text
