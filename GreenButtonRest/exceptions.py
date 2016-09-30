class GreenException(Exception):
    message = None
    code = None

    def __init__(self, result):
        self.message = result.content[0]
        self.code = result.status_code

    def __str__(self):
        return "GreenButton API Error: ".format(self.message)
