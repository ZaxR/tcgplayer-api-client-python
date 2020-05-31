import requests


class BearerAuth(requests.auth.AuthBase):
    AUTHORIZATION_BASE_URL = ""
    TOKEN_URL = "https://api.tcgplayer.com/token"

    def __init__(self, token=None, public_key=None, private_key=None):
        self.token = token or self._get_access_token(public_key, private_key)

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

    @staticmethod
    def _get_access_token(public_key, private_key):
        response = requests.post(
            BearerAuth.TOKEN_URL,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"},
            data=(f"grant_type=client_credentials"
                  f"&client_id={public_key}&"
                  f"client_secret={private_key}")
        )
        # {
        #   "access_token":"BEARER_TOKEN",
        #   "token_type":"bearer",
        #   "expires_in":1209599,
        #   "userName":"PUBLIC_KEY",
        #   ".issued":"Fri, 07 Jul 2017 16:47:46 GMT",
        #   ".expires":"Fri, 21 Jul 2017 16:47:46 GMT"
        # }

        return response.json()['access_token']
