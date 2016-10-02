import time

import requests


class HttpCustom:
    max_retries = 3
    sleep = 5
    num_calls_per_second = 10

    def _rate_limited(self):
        min_interval = 1.0 / float(self)

        def decorate(func):
            lsat_time_called = [0.0]

            def rate_limited_function(*args, **kwargs):
                elapsed = time.clock() - lsat_time_called[0]
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)
                ret = func(*args, **kwargs)
                lsat_time_called[0] = time.clock()
                return ret

            return rate_limited_function

        return decorate

    @_rate_limited(num_calls_per_second)
    def get(self, endpoint, args=None, mode=None):
        retries = 0
        while True:
            if retries > self.max_retries:
                return None
            try:
                headers = {'Accept-Encoding': 'gzip'}
                r = requests.get(endpoint, params=args, headers=headers)
                if mode is 'nojson':
                    return r
                else:
                    r_json = r.json()
                    # if we still hit the rate limiter, do not return anything so the call will be retried
                    if 'success' in r_json:  # this is for all normal API calls (but not the access token call)
                        if r_json['success'] == False:
                            print('error from http_lib.py: ' + str(r_json['errors'][0]))
                            if r_json['errors'][0]['code'] == '606':
                                print('error 606, rate limiter. Pausing, then trying again')
                                time.sleep(5)
                            else:
                                return r_json
                        else:
                            return r_json
                    else:
                        return r_json  # this is only for the access token call
            except Exception as e:
                print("HTTP Get Exception! Retrying.....")
                time.sleep(self.sleep_duration)
                retries += 1
