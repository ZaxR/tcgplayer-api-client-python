# Python imports
import json, logging, os, re, time
from datetime import datetime, timedelta
from functools import partial
from typing import Any, Dict, List, NamedTuple, Union

# 3rd Party imports
import requests

# Internal imports
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
        except json.JSONDecodeError:
            resp = Response(status_code=r.status_code, headers=r.headers)
        return resp


class TCGPlayerClient:
    f'''
    The TCGPlayerClient contains all components necessary to make calls to the
    TCGPlayer API using the requests library. It's methods are derived from the 
    file in api_specs/ corresponding to either the supplied or most recent API version.

    Args:
        auth (BearerAuth): token object used for API authentication
        headers (dict): extra headers to append to every API call (Optional)
        api_version (str): API version to use, ex. 'vx.x.x', if not supplied,
                           the most recent one will be used

    Attributes:
        client (requests.Session): requests client used for making HTTP requests
        version (str): version of the API to make calls to
        base_url (str): base_url that all API calls will have in common
        timer (datetime): timer used to delay API calls, so as to not exceed the API call limit
    '''

    API_SPEC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "api_specs"))
    MAX_PAGINATION_RESULTS = 100
    MIN_REQUEST_WAIT = 200 * 1000 # microseconds


    def __init__(self, auth: BearerAuth, headers: dict = None,
                 api_version: str = None, ):
        headers = headers or {}
        self.client = RequestsClient(auth=auth, headers=headers)
        self.version = api_version or self._get_latest_api_version()
        self.base_url = f"http://api.tcgplayer.com/{self.version}"
        # NOTE: Set timer behind by MIN_REQUEST_WAIT to ensure no initial wait
        self.timer = datetime.now() - timedelta(microseconds=TCGPlayerClient.MIN_REQUEST_WAIT)

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


    def _api_call(self, http_method, url, query_params={}, body_params={}):
        """
        Internal function used to perform API calls based on given arguments.
            - Wraps the timer check to avoid exceeding API call limit.
            - Wraps request client for different HTTP methods
            - Filters and returns JSON data from response

        Returns:
            dict: 
        """
        # Implements internal timer w/ sleep to avoid hitting API call limit
        now = datetime.now()
        time_diff = now - self.timer
        if time_diff.microseconds < TCGPlayerClient.MIN_REQUEST_WAIT:
            time.sleep((TCGPlayerClient.MIN_REQUEST_WAIT - time_diff.microseconds)/1000000)

        # Execute API Call
        # Will raise HTTPError: "405 Client Error: Method Not Allowed for url"
        # if a bad http_method is given
        # TODO: See why POST calls aren't working ATM
        # See: https://requests.readthedocs.io/en/master/api/?highlight=.request#requests.Session.request
        if http_method == "POST":
            response = self.client.request(http_method, url, params=query_params, data=body_params)
        else:
            response = self.client.request(http_method, url, params=query_params)

        if response.status_code != 200:
            raise UnexpectedStatusCode

        response_data = response.json
        if not response_data:
            raise ValueError(f"No data returned from {http_method} {url} with query_params:\n{query_params}")

        return response_data


    def _get_latest_api_version(self):
        """
        Function to read latest API version from api_specs.

        Returns:
            str: 'v[API_VERSION]'
        """
        return max(os.listdir(self.API_SPEC_PATH))[:-5]  # strip ending ".json"


    def _method_factory(self, service_name: str, uri: str, http_method: str):
        """
        Factory function to create class instance methods from api_specs
        that executes corresponding API call with given arguments as parameters.
        
        Returns:
            func: (**kwargs)   
        """
        def service_name(**parameters):
            """
            Generically named function designed to act as each individual 
            service provided by the API.
                - Formats API call based on the given arguments of
                  itself & it's _method_factory
            
            Returns:
                dict: {
                    "totalItems": int, NOTE: Not always present 
                    "success": bool,
                    "results": list
                }    
            """
            def format_query_parameters(parameters):
                result = {}
                for (key, value) in parameters.items():
                    result[snake_to_camel_case(key)] = value
                return result
        
            # NOTE: parameters combines both path parameters and query parameters
            # this is for convenience, 
            # but assumes that path params and query params can't collide.
            # NOTE: body_params are not being taken into consideration at this time...
            # Any attempt to include them will result in them being passed as query_params,
            # which means that best case, they get ignored, worst case, they cause an error
            # Hopefully it will be a feature implemented in future versions
            path_params = {}
            query_params = {}
            # If '{' in the uri, then it must have path_params
            if "{" in uri:
                uri_path_params = re.findall(r"\{(.*?)\}", uri)
                for param in uri_path_params:
                    if param in parameters:
                        path_params[param] = parameters.pop(param)
                    else:
                        raise KeyError("URI path parameter", param, "not found in supplied parameters")
                query_params = format_query_parameters(parameters)
            else:
                query_params = format_query_parameters(parameters)
            
            # NOTE: If a limit is not supplied in initial query_params,
            # include the maximum limit in case of paginated results,
            # if not included, the default limit == 10, often causing extra calls
            if "limit" not in query_params:
                query_params["limit"] = TCGPlayerClient.MAX_PAGINATION_RESULTS
            
            # Format URL based on parameters
            request_uri = uri.format(**parameters)
            request_url = f"{self.base_url}{request_uri}"

            # Make API call
            response = self._api_call(http_method, request_url, query_params)

            # Loops through pages and collects results
            if response["success"] == True and "totalItems" in response:
                num_results = len(response["results"])
                # Limit is based on either supplied "limit" or response's "totalItems"
                limit = response["totalItems"]
                if "limit" in parameters and parameters["limit"] < limit:
                    limit = parameters["limit"]
                # Take into account supplied offset
                base_offset = 0
                if "offset" in parameters:
                    base_offset = parameters["offset"]
                # Loop while there are fewer results than desired, or until unsuccessful request
                while limit > num_results:
                    new_offset = num_results + base_offset
                    new_params = {
                        **query_params, 
                        "offset": new_offset,
                        "limit": min(limit-new_offset, TCGPlayerClient.MAX_PAGINATION_RESULTS)
                    }
                    new_response = self._api_call(http_method, request_url, new_params)
                    
                    if new_response["success"] == True:
                        # Append new results to existing ones in response object
                        response["results"].extend(new_response["results"])
                        num_results += len(new_response["results"])
                    else:
                        break

            # TODO create a class for the response

            return response

        return service_name
