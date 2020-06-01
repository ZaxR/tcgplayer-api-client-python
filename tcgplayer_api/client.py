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
    # TODO: parameterize version
    BASE_URL = "http://api.tcgplayer.com/{api_version}"

    def __init__(self, auth: BearerAuth, headers: dict = None,
                 version: str = None, ):
        headers = headers or {}
        self.client = RequestsClient(auth=auth, headers=headers)
        self.version = version or "v1.37.0"  # _get_latest_api_version()
        self.base_url = self.BASE_URL.format(api_version=self.version)
        self.services = {}

        api_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                f"api_specs/{self.version}.json"))
        with open(api_file, "r") as f:
            api_data = json.load(f)

        for service in api_data:
            service_name = service["name"]
            uri = service["uri"]
            http_method = service["http_method"]
            func_name = words_to_snake_case(service_name)
            # Call API Method directly as a class method
            self.__dict__[func_name] = partial(self._call, service_name, uri, http_method)

    def _call(self, service_name, uri, http_method, path_params=None, **query_params):
        # TODO: change this so path_params doesn't have to be a dict
        path_params = path_params or {}

        # Prepare API call parameters
        request_uri = uri.format(**path_params)
        request_url = f"{self.base_url}{request_uri}"

        # Execute API Call
        # Will raise HTTPError: "405 Client Error: Method Not Allowed for url"
        # if a bad http_method is given
        # TODO: See why posts aren't working ATM
        response = self.client.request(http_method, request_url, params=query_params)

        if response.status_code != 200:
            raise UnexpectedStatusCode

        resp_json = response.json
        if not resp_json:
            raise ValueError("No data returned.")

        # TODO, loop through pages and collect results
        # TODO create a class for the response

        return resp_json
