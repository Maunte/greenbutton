import time

import requests

from GreenButtonRest.exceptions import GreenException


class GreenClient:
    host = None
    token = None
    expires_in = None
    valid_until = None
    token_type = None
    scope = None
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
                    "ApplicationInformation": self.get_application_info,
                }
                result = method_map[method](*args, **kargs)
                self.API_CALLS_MADE += 1
            except GreenException as e:
                '''
                601 -> auth token not valid
                602 -> auth token expired
                '''
                if e.code in ['601', '602']:
                    self.authenticate()
                    continue
                else:
                    raise Exception({'message': e.message, 'code': e.code})
            break
        return result

    def authenticate(self):
        if self.valid_until is not None and \
                                self.valid_until - time.time() >= 60:
            return
        self.token = "Bearer 2a85f4bd-30db-4b7d-8f41-b046b0566cb3"

    def get_application_info(self, published_max=None, published_min=None, updated_max=None, updated_min=None,
                             max_results=None, start_index=None, depth=None):
        self.authenticate()
        args = {
            "authorization": self.token
        }
        if published_max is not None:
            args["published-max"] = published_max
        if published_min is not None:
            args["published-min"] = published_min
        if updated_max is not None:
            args["updated-max"] = updated_max
        if updated_min is not None:
            args["updated-min"] = updated_min
        if max_results is not None:
            args["max-results"] = max_results
        if start_index is not None:
            args["start-index"] = start_index
        if depth is not None:
            args["depth"] = depth

        result = requests.get(url=self.host + "/ApplicationInformation", headers=args)
        return result
