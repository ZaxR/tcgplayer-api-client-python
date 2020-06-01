TCGPlayer-API
========================================

A Python client library for the [TCGPlayer API](https://docs.tcgplayer.com/docs)


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