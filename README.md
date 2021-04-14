# TCGPlayer-API
 
<a href="https://pypi.org/project/tcgplayer-api/"><img src="https://img.shields.io/pypi/v/tcgplayer-api?style=for-the-badge" alt="latest release" /></a>
<a href="https://pypi.org/project/tcgplayer-api/"><img src="https://img.shields.io/pypi/pyversions/tcgplayer-api?style=for-the-badge" alt="supported python versions" /></a>
<a href="https://pypi.org/project/tcgplayer-api/"><img src="https://img.shields.io/pypi/status/tcgplayer-api?style=for-the-badge" alt="package status" /></a>
<a href="https://github.com/ZaxR/tcgplayer-api-client-python/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/tcgplayer-api?style=for-the-badge" alt="license" /></a>

A Python client library for the [TCGPlayer API](https://docs.tcgplayer.com/docs)


# Installation


```bash
pip install tcgplayer-api
```

 See the table below for officially supported Python versions:

| tcgplayer-api | Python |
|:-------------:|:------:|
|     0.1.0     |  >=3.6 |

Note: the latest version of tcgplayer-api will only be compatible with newer versions of Python. This is to allow tcgplayer-api to take advantage of the latest language/library features and to reduce the technical debt of maintaining tcgplayer-api.

# Table of Contents
- ### [Basic Usage](#basic-usage)
- ### [Advanced Usage](#advanced-usage)
  - #### [BearerAuth](#bearer-auth)
  - #### [TCGPlayerClient](#tcgplayer-client)
- ### [Road map to v1.0.0](#road-map-to-v1.0.0)

# Basic Usage


```python
>>> from tcgplayer_api.auth import BearerAuth
>>> from tcgplayer_api.client import TCGPlayerClient


>>> PUBLIC_KEY = "[YOUR_PUBLIC_KEY]"
>>> PRIVATE_KEY = "[YOUR_PRIVATE_KEY]"
>>> auth = BearerAuth(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

>>> client = TCGPlayerClient(auth=auth)
>>> client.list_all_categories()
{'totalItems': 61,
 'success': True,
 'errors': [],
 'results': [{'categoryId': 55,
   'name': 'Architect TCG',
   'modifiedOn': '2018-09-17T15:21:54.233',
   'displayName': 'Architect TCG',
   'seoCategoryName': 'Architect TCG',
   'sealedLabel': 'Sealed Products',
   'nonSealedLabel': 'Singles',
   'conditionGuideUrl': 'https://store.tcgplayer.com/',
   'isScannable': True,
   'popularity': 0},
  ...
 ]
}
```

# Advanced Usage
This package is comprised of two essential classes that encapsulate all of the functionality for API accessibility,

- ## Bearer Auth
  ### Initialization Arguments:
  - `token (str)` - bearer token provided by API for call authorization
  - `token_expiration (str)` - expiration date used to help properly manage tokens per API specs (format: "%a, %d %b %Y %H:%M:%S %Z")
  - `public_key (str)` - public key provided by API manager for access tokens 
  - `private_key (str)` - private key provided by API manager for access tokens

  ### Usage:
  - `token:` No validation will be made and calls will be executed using given token
    ```python
    >>> from tcgplayer_api.auth import BearerAuth

    auth = BearerAuth(token="[YOUR_GENERATED_TOKEN]") 
    ```
  - `public_key & private_key:` API call will be made using these values to generate and store a `token`
    ```python
    >>> from tcgplayer_api.auth import BearerAuth

    >>> auth = BearerAuth(
    >>>   public_key = "[YOUR_PUBLIC_KEY]",
    >>>   private_key = "[YOUR_PRIVATE_KEY]"
    >>> )
    ```
  - `all args:` will utilize `token`, if `token_expiration` is valid; otherwise generates `token` from keys


- ## TCGPlayer Client
  ### Initialization Arguments:
  - `auth (BearerAuth)` - BearerAuth providing all necessary authorization information
  - `headers (dict)` [OPTIONAL] - extra headers to append to all requests made by the client
  - `api_version (str)` [OPTIONAL] - desired API version to use, uses latest if unspecified

  ### Usage:
  ```python
  >>> from tcgplayer_api.auth import BearerAuth
  >>> from tcgplayer_api.client import TCGPlayerClient

  >>> auth = BearerAuth(...) # see above 

  >>> client = TCGPlayerClient(auth=auth)

  >>> response = client.list_all_categories()
  ```
  All API calls are made through functions invoked from the client object. Names of available methods can be found in the API specs in the corresponding file in `tcgplayer_api/api_specs`, named according to version number.

  Currently there is no documentation of these methods' arguments in this package, nor any error handling for invalid or insufficient arguments, but it is a future goal to have everything fully documented and all errors properly handled. Until then, common sense and the [documentation of the TCGPlayer API](https://docs.tcgplayer.com/reference) can help you figure out what you need to do to get it working for you.

  ### Response:
  Responses will be in the format:
  ```
  {
    "totalItems": int,
    "success": bool,
    "results": [
      {
        ...data
      }
    ]
  }
  ```
  NOTE: "totalItems" is not always present

# Road map to v1.0.0
- [ ] Fix support for POST and other request types besides GET
- [x] Add timer functionality to stop from exceeding API call limit
- [x] Add pagination support for responses
- [x] Add module/func docstrings
- [x] Add basic documentation
- [ ] Add path, query & body parameters to v1.37.0.json
- [ ] Improve endpoint methods' docstrings to include arg info
- [ ] Add more meaningful error messages when required params are missing or for various status codes
- [ ] Add tests for each endpoint method
- [ ] Add LICENSE information
- [ ] Add handling & storing of credentials in JSON file
- [ ] Add support for app_name to be used in User-Agent header, as per API best practices

