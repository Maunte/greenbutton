class GreenException(Exception):
    message = None
    code = None

    def __init__(self, exc={'message': None, 'code': None}):
        self.msg = exc['message']
        self.code = exc['code']

    def __str__(self):
        return "GreenButton API Error Code {}: {}".format(self.code, self.msg)
