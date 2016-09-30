import requests

from GreenButtonRest.exceptions import GreenException


class GreenClient:
    host = None
    token = None
    API_CALLS_MADE = 0
    API_LIMIT = None

    def __init__(self, api_limit=None):
        self.host = "https://services.greenbuttondata.org:443/DataCustodian/espi/1_1/resource"
        self.API_LIMIT = api_limit

    def execute(self, method, *args, **kargs):
        result = None
        for i in range(0, 10):
            try:

                method_map = {
                    "application_information": self.get_application_info,
                    "application_information_by_id": self.get_application_info_id,
                    "authorization": self.get_authorization,
                    "authorization_id": self.get_authorization_id,
                    "batch_bulk": self.get_batch_bulk,

                }
                result = method_map[method](*args, **kargs)
                self.API_CALLS_MADE += 1
            except GreenException as e:
                '''
                601 -> auth token not valid
                602 -> auth token expired
                '''
                if e.code in [601, 602]:
                    self.authenticate()
                    continue
                else:
                    raise Exception({'message': e.message, 'code': e.code})
            break
        return result

    def authenticate(self):
        self.token = "Bearer 2a85f4bd-30db-4b7d-8f41-b046b0566cb3"
        # self.token = ""

    # --------- APPLICATION INFORMATION ---------

    def get_application_info(self, published_max=None, published_min=None, updated_max=None, updated_min=None,
                             max_results=None, start_index=None, depth=None):
        self.authenticate()
        headers = {
            "authorization": self.token
        }
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

        result = requests.get(url=self.host + "/ApplicationInformation", headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result

    def get_application_info_id(self, application_information_id):
        self.authenticate()
        headers = {
            "authorization": self.token
        }
        result = requests.get(url=self.host + "/ApplicationInformation/" + str(application_information_id),
                              headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result

    # --------- AUTHORIZATION ---------

    def get_authorization(self, published_max=None, published_min=None, updated_max=None, updated_min=None,
                          max_results=None, start_index=None, depth=None):
        self.authenticate()
        headers = {
            "authorization": self.token
        }
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

        result = requests.get(url=self.host + "/Authorization", headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result

    def get_authorization_id(self, application_information_id):
        self.authenticate()
        headers = {
            "authorization": self.token
        }
        result = requests.get(url=self.host + "/Authorization/" + str(application_information_id),
                              headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result

    # --------- BATCH ---------

    def get_batch_bulk(self, bulk_id, published_max=None, published_min=None, updated_max=None, updated_min=None,
                       max_results=None, start_index=None, depth=None):
        self.authenticate()
        headers = {
            "authorization": self.token
        }
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

        result = requests.get(url=self.host + "/Batch/Bulk/" + str(bulk_id), headers=headers)

        if result is None: raise Exception("Empty Response")
        if result.status_code == 403: raise GreenException(result)

        return result

    def get_batch_subscription(self):
        self.authenticate()
        return None

    def get_batch_retail_customer(self):
        self.authenticate()
        return None

    def get_batch_subscription_usage(self):
        self.authenticate()
        return None
