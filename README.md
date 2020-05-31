TCGPlayer-API
========================================

A Python client library for the [TCGPlayer API](https://docs.tcgplayer.com/docs)


Example Usage
==============

```
>>> from auth import BearerAuth
>>> from client import TCGPlayerClient


>>> PUBLIC_KEY = "x"
>>> PRIVATE_KEY = "y"
>>> auth = BearerAuth(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)

>>> client = TCGPlayerClient(auth=auth)
>>> client.get_x(1)
{'totalItems': 265,
 'success': True,
 'errors': [],
 'results': [{'groupId': 2655,
   'name': 'Double Masters',
   'abbreviation': '',
   'isSupplemental': False,
   'publishedOn': '2020-08-07T00:00:00',
   'modifiedOn': '2020-05-29T19:11:25.973',
   'categoryId': 1},
  ...
 ]
}
```