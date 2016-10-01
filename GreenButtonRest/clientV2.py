# -*- coding: utf-8 -*-

"""
greenbutton.client
~~~~~~~~~~~~

This module implements the GreenButton API.

:copyright: (c) 2016 by Eric Proulx.
"""

import requests

from GreenButtonRest.exceptions import GreenException

"""Constructs and sends a :class:`Request <Request>`.

Usage::

  >>> from GreenButtonRest.clientV2 import GreenClient
  >>> gc = GreenClient()
  >>> execute = gc.execute("authorization")
  >>> print(execute.text)
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
                    "application_information_by_id": self.get_application_info_id,
                    "authorization": self.get_authorization,
                    "authorization_id": self.get_authorization_id,
                    "batch_bulk": self.get_batch_bulk,
                    "batch_subscription": self.get_batch_subscription,
                    "batch_retail": self.get_batch_retail_customer,
                    "batch_subscription_usage": self.get_batch_subscription_usage

                }
                result = method_map[method](*args, **kwargs)
                self.API_CALLS_MADE += 1
            except GreenException as e:
                # TODO: Identify authentication errors
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
        :param max_results: (optional) The upper bound on the number of entries to be contained in a reply to this response.
        :type max_results: long
        :param start_index: (optional) The one based offset in the DataCustodian's collection of Application Information that should be transferred as the first entry of this request.
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

    def get_application_info(self, published_max=None, published_min=None, updated_max=None, updated_min=None,
                             max_results=None, start_index=None, depth=None):
        """ Gets application information.

        :param published_max: (optional) The upper bound on the published date of the Application Information.
        :type published_max: date
        :param published_min: (optional) The lower bound on the published date of the Application Information.
        :type published_min: date
        :param updated_max: (optional) The upper bound on the updated date of the Application Information.
        :type updated_max: date
        :param updated_min: (optional) The lower bound on the updated date of the Application Information.
        :type updated_min: date
        :param max_results: (optional) The upper bound on the number of entries to be contained in a reply to this response.
        :type max_results: long
        :param start_index: (optional) The one based offset in the DataCustodian's collection of Application Information that should be transferred as the first entry of this request.
        :type start_index: long
        :param depth: (optional) The maximum number of entries to be transferred in the response to this request.
        :type depth: long
        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        result = requests.get(url=self.host + "/ApplicationInformation", headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_application_info_id(self, application_information_id):
        """ Gets application information.

        :param application_information_id: (required) The Id of the Application Information to be retrieved.
        :type application_information_id: str
        :return: xml result
        :rtype text/xsl
        """

        self.authenticate()
        headers = {
            "authorization": self.token
        }
        result = requests.get(url=self.host + "/ApplicationInformation/" + str(application_information_id),
                              headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- AUTHORIZATION ---------

    def get_authorization(self, published_max=None, published_min=None, updated_max=None, updated_min=None,
                          max_results=None, start_index=None, depth=None):
        """ Gets authorization information.

        :param published_max: (optional) The upper bound on the published date of the Application Information.
        :type published_max: date
        :param published_min: (optional) The lower bound on the published date of the Application Information.
        :type published_min: date
        :param updated_max: (optional) The upper bound on the updated date of the Application Information.
        :type updated_max: date
        :param updated_min: (optional) The lower bound on the updated date of the Application Information.
        :type updated_min: date
        :param max_results: (optional) The upper bound on the number of entries to be contained in a reply to this response.
        :type max_results: long
        :param start_index: (optional) The one based offset in the DataCustodian's collection of Application Information that should be transferred as the first entry of this request.
        :type start_index: long
        :param depth: (optional) The maximum number of entries to be transferred in the response to this request.
        :type depth: long
        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        result = requests.get(url=self.host + "/Authorization", headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_authorization_id(self, authorization_id):
        """ Gets authorization by id.

        :param authorization_id: (required) Id of the Authorization to be retrieved.
        :type authorization_id: str
        :return: xml result
        :rtype text/xsl
        """

        self.authenticate()
        headers = {
            "authorization": self.token
        }
        result = requests.get(url=self.host + "/Authorization/" + str(authorization_id),
                              headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    # --------- BATCH ---------

    def get_batch_bulk(self, bulk_id, published_max=None, published_min=None, updated_max=None, updated_min=None,
                       max_results=None, start_index=None, depth=None):
        """ Gets batch information.

        :param bulk_id: (required) The Bulk Id as specified in the OAuth2 SCOPE string.
        :type bulk_id: str
        :param published_max: (optional) The upper bound on the published date of the Application Information.
        :type published_max: date
        :param published_min: (optional) The lower bound on the published date of the Application Information.
        :type published_min: date
        :param updated_max: (optional) The upper bound on the updated date of the Application Information.
        :type updated_max: date
        :param updated_min: (optional) The lower bound on the updated date of the Application Information.
        :type updated_min: date
        :param max_results: (optional) The upper bound on the number of entries to be contained in a reply to this response.
        :type max_results: long
        :param start_index: (optional) The one based offset in the DataCustodian's collection of Application Information that should be transferred as the first entry of this request.
        :type start_index: long
        :param depth: (optional) The maximum number of entries to be transferred in the response to this request.
        :type depth: long
        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        result = requests.get(url=self.host + "/Batch/Bulk/" + str(bulk_id), headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_batch_subscription(self, subscription_id, published_max=None, published_min=None, updated_max=None,
                               updated_min=None,
                               max_results=None, start_index=None, depth=None):
        """ Gets batch subscription by subscriptionId.

        :param subscription_id: (required) The Subscription's Id.
        :type subscription_id: str
        :param published_max: (optional) The upper bound on the published date of the Application Information.
        :type published_max: date
        :param published_min: (optional) The lower bound on the published date of the Application Information.
        :type published_min: date
        :param updated_max: (optional) The upper bound on the updated date of the Application Information.
        :type updated_max: date
        :param updated_min: (optional) The lower bound on the updated date of the Application Information.
        :type updated_min: date
        :param max_results: (optional) The upper bound on the number of entries to be contained in a reply to this response.
        :type max_results: long
        :param start_index: (optional) The one based offset in the DataCustodian's collection of Application Information that should be transferred as the first entry of this request.
        :type start_index: long
        :param depth: (optional) The maximum number of entries to be transferred in the response to this request.
        :type depth: long
        :return: xml result
        :rtype text/xsl
        """

        headers = self.build_params(published_max, published_min, updated_max, updated_min, max_results, start_index,
                                    depth)

        result = requests.get(url=self.host + "/Batch/Subscription/" + str(subscription_id), headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result.text

    def get_batch_retail_customer(self, retail_customer_id, published_max=None, published_min=None, updated_max=None,
                                  updated_min=None,
                                  max_results=None, start_index=None, depth=None):
        """ Gets batch retail customer usage.

        :param retail_customer_id: (required) The Retail Customer's Id.
        :type retail_customer_id: str
        :param published_max: (optional) The upper bound on the published date of the Application Information.
        :type published_max: date
        :param published_min: (optional) The lower bound on the published date of the Application Information.
        :type published_min: date
        :param updated_max: (optional) The upper bound on the updated date of the Application Information.
        :type updated_max: date
        :param updated_min: (optional) The lower bound on the updated date of the Application Information.
        :type updated_min: date
        :param max_results: (optional) The upper bound on the number of entries to be contained in a reply to this response.
        :type max_results: long
        :param start_index: (optional) The one based offset in the DataCustodian's collection of Application Information that should be transferred as the first entry of this request.
        :type start_index: long
        :param depth: (optional) The maximum number of entries to be transferred in the response to this request.
        :type depth: long
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

    def get_batch_subscription_usage(self, subscription_id, usage_point_id, published_max=None, published_min=None,
                                     updated_max=None,
                                     updated_min=None,
                                     max_results=None, start_index=None, depth=None):
        """ Gets batch information.

        :param subscription_id: (required) The Subscription's Id.
        :type subscription_id: str
        :param usage_point_id: (required) The UsagePoint's Id.
        :type usage_point_id: str
        :param published_max: (optional) The upper bound on the published date of the Application Information.
        :type published_max: date
        :param published_min: (optional) The lower bound on the published date of the Application Information.
        :type published_min: date
        :param updated_max: (optional) The upper bound on the updated date of the Application Information.
        :type updated_max: date
        :param updated_min: (optional) The lower bound on the updated date of the Application Information.
        :type updated_min: date
        :param max_results: (optional) The upper bound on the number of entries to be contained in a reply to this response.
        :type max_results: long
        :param start_index: (optional) The one based offset in the DataCustodian's collection of Application Information that should be transferred as the first entry of this request.
        :type start_index: long
        :param depth: (optional) The maximum number of entries to be transferred in the response to this request.
        :type depth: long
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
