class CreateException(Exception):
    pass


class ExpectedStatusCodeError(Exception):
    def __init__(self, response, status_code):
        self.response = response
        self.status_code = status_code
        print ('Expected Status Code is {status_code} But in response we get {response} Status Code'.format(
            status_code=status_code,
            response=response.status_code))


class ResourceNotFound(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return repr(self.response)