TCGPlayer-API
========================================

A Python client library for the [TCGPlayer API](https://docs.tcgplayer.com/docs)


Installation
=============

```bash
pip install tcgplayer-api
```

Note that the latest version of tcgplayer-api will only be compatible with newer version of Python. This is to allow tcgplayer-api to take advantage of the latest language/library features and to reduce the technical debt of maintaining tcgplayer-api. See the table below for officially supported versions:

| tcgplayer-api | Python |
|:-------------:|:------:|
|     0.0.1     |  >=3.6 |


Example Usage
==============

```
>>> from tcgplayer_api.auth import BearerAuth
>>> from tcgplayer_api.client import TCGPlayerClient


>>> PUBLIC_KEY = "x"
>>> PRIVATE_KEY = "y"
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