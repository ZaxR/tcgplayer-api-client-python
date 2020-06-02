import os
import json
import logging
from functools import partial
from json import JSONDecodeError
from typing import Any, Dict, List, NamedTuple, Union

import requests

from tcgplayer_api.auth import BearerAuth
from tcgplayer_api.utils import words_to_snake_case


logger = logging.getLogger(__name__)


# TODO: Consider using werkzeug exceptions
class UnexpectedStatusCode(Exception):
    pass


class HttpMethodError(Exception):
    pass


class Response(NamedTuple):
    status_code: int
    headers: Dict[str, str]
    json: Union[List[Dict[str, Any]], Dict[str, Any]] = None


class RequestsClient:
    """Wrapper around requests to simplify interaction with JSON REST APIs"""

    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    def __init__(self, auth: BearerAuth, headers: dict = None):
        _headers = dict(self.DEFAULT_HEADERS)
        if headers is not None:
            _headers.update(headers)

        s = requests.Session()
        s.auth = auth
        self.headers = _headers
        self.session = s

    def __repr__(self):
        return "RequestsClient"

    def request(self, method: str, url: str, **kwargs) -> Response:
        req_headers = dict(self.headers)
        if "headers" in kwargs:
            headers_to_add = kwargs.pop("headers")
            req_headers.update(headers_to_add)

        r = self.session.request(method, url, headers=req_headers, **kwargs)
        r.raise_for_status()

        try:
            resp = Response(status_code=r.status_code, headers=r.headers, json=r.json())
        except JSONDecodeError:
            resp = Response(status_code=r.status_code, headers=r.headers)
        return resp


class TCGPlayerClient:
    API_SPEC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "api_specs"))

    def __init__(self, auth: BearerAuth, headers: dict = None,
                 api_version: str = None, ):
        headers = headers or {}
        self.client = RequestsClient(auth=auth, headers=headers)
        self.version = api_version or self._get_latest_api_version()
        self.base_url = f"http://api.tcgplayer.com/{self.version}"
        self.services = {}

        api_file = f"{self.API_SPEC_PATH}/{self.version}.json"
        with open(api_file, "r") as f:
            api_data = json.load(f)

        # Add each API object as a class instance method
        for service in api_data:
            func_name = words_to_snake_case(service["name"])
            method = self._method_factory(func_name, service["uri"], service["http_method"])
            method.__name__ = method.__qualname__ = func_name
            method.__doc__ = service.get("description")
            self.__dict__[func_name] = method

    def _get_latest_api_version(self):
        return max(os.listdir(self.API_SPEC_PATH))[:-5]  # strip ending ".json"

    def _method_factory(self, service_name: str, uri: str, http_method: str):
        """Factory function to create class instance methods from api_specs."""
        def service_name(**parameters):
            # Note that parameters combined path parameters and query parameters
            # this is for convenience,
            # but assumes that path params and query params can't collide.
            request_uri = uri.format(**parameters)
            request_url = f"{self.base_url}{request_uri}"

            # Execute API Call
            # Will raise HTTPError: "405 Client Error: Method Not Allowed for url"
            # if a bad http_method is given
            # TODO: See why posts aren't working ATM; "params" might need to be "data"
            # See: https://requests.readthedocs.io/en/master/api/?highlight=.request#requests.Session.request
            response = self.client.request(http_method, request_url, params=parameters)

            if response.status_code != 200:
                raise UnexpectedStatusCode

            resp_json = response.json
            if not resp_json:
                raise ValueError("No data returned.")

            # TODO, loop through pages and collect results
            # TODO create a class for the response

            return resp_json

        return service_name
