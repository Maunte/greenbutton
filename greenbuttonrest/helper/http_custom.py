import time

import requests

from greenbuttonrest.helper.exceptions import GreenException


class HttpCustom:
    max_retries = 2
    sleep_duration = 5
    num_calls_per_second = 10

    def _rate_limited(self):
        min_interval = 1.0 / float(self)

        def decorate(func):
            last_time_called = [0.0]

            def rate_limited_function(*args, **kwargs):
                elapsed = time.clock() - last_time_called[0]
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                ret = func(*args, **kwargs)
                last_time_called[0] = time.clock()
                return ret

            return rate_limited_function

        return decorate

    @_rate_limited(num_calls_per_second)
    def get(self, endpoint, headers):
        retries = 0
        while True:
            if retries > self.max_retries:
                return None
            try:
                r = requests.get(endpoint, headers=headers)
                if r is None:
                    raise Exception("Empty Response")
                elif r.status_code == 403 or r.status_code == 400:
                    raise GreenException(r)
                else:
                    return r.text

            except Exception as e:
                print("HTTP Get Exception! Retrying.....")
                time.sleep(self.sleep_duration)
                retries += 1
