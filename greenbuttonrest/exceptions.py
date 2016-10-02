import json


class GreenException(Exception):
    message = None
    code = None

    def __init__(self, result):
        self.message = json.loads(result.text)["error_description"]
        self.code = result.status_code

    def __str__(self):
        return "GreenButton API Error: ".format(self.message)
