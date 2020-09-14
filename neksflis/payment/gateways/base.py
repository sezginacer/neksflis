import requests


class BaseResponse:
    def __init__(self, request, response):
        super().__init__()
        self.raw_request = request.body
        self.raw_response = response.text
        as_json = self.to_json(response)
        self.as_json = self.normalize_response(as_json)
        self.success = self.is_succeeded(response)
        self.error_message = self.get_error_message(self.as_json)
        self.elapsed = response.elapsed
        self.card_token = None

    def to_json(self, response):
        try:
            return response.json()
        except ValueError:
            return {}

    def normalize_response(self, json_data):
        return json_data

    def is_succeeded(self, response):
        raise NotImplementedError

    def get_error_message(self, json_data):
        raise NotImplementedError

    def __str__(self):
        return f'success: {self.success}, response: {self.as_json}'


class BaseGateway:
    response_class = BaseResponse
    connect_timeout = 5
    read_timeout = 30

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def send_request(self, method, data=None, **kwargs):
        url = kwargs.pop('url', self.url)
        request = requests.Request(
            method=method,
            url=url,
            data=data,
            headers=self.get_headers(),
            auth=self.get_auth(),
        )
        request = request.prepare()
        response = None
        try:
            response = self.session.send(
                request, timeout=(self.connect_timeout, self.read_timeout))
            response.raise_for_status()
        except requests.RequestException:
            if response is None:
                response = requests.Response()
        response_class = kwargs.pop('response_class', self.response_class)
        return response_class(request=request, response=response)

    def get_headers(self):
        return {}

    def get_auth(self):
        return None

    def charge(self, **kwargs):
        raise NotImplementedError

    def get_card_token(self, **kwargs):
        raise NotImplementedError
