import logging
from json import JSONDecodeError
from typing import Any, Dict, List, NamedTuple, Union

import requests

from auth import BearerAuth


logger = logging.getLogger(__name__)


# TODO: Consider using werkzeug exceptions
class UnexpectedStatusCode(Exception):
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

    def get(self, url: str, **kwargs) -> Response:
        return self._request("get", url, **kwargs)

    def head(self, url: str, **kwargs) -> Response:
        return self._request("head", url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        return self._request("post", url, **kwargs)

    def _request(self, method: str, url: str, **kwargs) -> Response:
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
    BASE_URL = "http://api.tcgplayer.com/v1.32.0"

    def __init__(self, auth: BearerAuth, headers: dict = None):
        headers = headers or {}
        self.client = RequestsClient(auth=auth, headers=headers)

    # TODO: rename method and properly parameterize path_params and body_params
    def get_x(self, category_id: str, limit: int = 16):
        url = self.BASE_URL + f"/catalog/categories/{category_id}/groups"
        payload = {"limit": limit}
        resp: Response = self.client.get(url, params=payload)

        if resp.status_code != 200:
            raise UnexpectedStatusCode

        x = resp.json
        if not x:
            raise ValueError("No x found.")

        # TODO, loop through pages and collect results
        # TODO create a class for the response

        return x
