# Python imports
from datetime import datetime, timedelta

# 3rd party imports
import requests


class BearerAuth(requests.auth.AuthBase):
    '''
    The BearerAuth object contains all necessary data for API authentication

    Args:
        token (str): token string generated from TCGPlayer API
        token_expiration (str): token expiration string (format in `EXPIRATION_FORMAT_STR`)
        public_key (str): public key given to the user by TCGPlayer API management
        private_key (str): private key given to the user by TCGPlayer API management

    Attributes:
        token (str): token string generated from TCGPlayer API
        expires (datetime): token expiration time
    '''
    EXPIRATION_FORMAT_STR = "%a, %d %b %Y %H:%M:%S %Z"
    MIN_TIME_TO_EXPIRATION = timedelta(hours=6)
    TOKEN_URL = "https://api.tcgplayer.com/token"


    def __init__(self, 
                 token: str = None,
                 token_expiration: str = None, 
                 public_key: str = None, 
                 private_key: str = None
                ):
        expires = None
        if token_expiration:
            expires = datetime.strptime(token_expiration, BearerAuth.EXPIRATION_FORMAT_STR) 
        if token and expires and self._check_expiration(expires):
            self.token = token
            self.expires = expires
        elif token:
            # NOTE: Kept here for backwards compatability,
            #       but doesn't handle invalid tokens
            # TODO: Make a test call with token to test validity...
            self.token = token
        elif public_key and private_key:
            token_data = self._get_access_token(public_key, private_key)
            self.token = token_data["access_token"]
            self.expires = datetime.strptime(token_data[".expires"], BearerAuth.EXPIRATION_FORMAT_STR)
        else:
            raise ValueError("Invalid arguments passed to tcgplayer_api.auth.BearerAuth")
 

    def __call__(self, r):
        """
        Internal function used by requests.Session to generate
        the appropriate (and necessary) authorization headers

        Args:
            r (requests.Request): Request object being constructed for the client

        Returns:
            requests.Request: the updated Request object with proper authorization

        """
        r.headers["authorization"] = "Bearer " + self.token
        return r


    @staticmethod
    def _check_expiration(expiration: datetime) -> bool:
        """
        Function to determine whether the given date is within 
        BearerAuth.MIN_TIME_TO_EXPIRATION from datetime.now()

        Args:
            expiration (datetime): Expiration time of current access token

        Returns:
            bool: Whether or not a new token is needed

        """
        result = True
        expires_in = expiration - datetime.now()
        if expires_in < BearerAuth.MIN_TIME_TO_EXPIRATION:
            result = False
        return result


    @staticmethod
    def _get_access_token(public_key, private_key):
        """
        Function to generate access token from API, given user's keys

        Args:
            public_key (str): public key provided by API manager
            private_key (str): private key provided by API manager

        Returns:
            dict: {
                "access_token":"BEARER_TOKEN",
                "token_type":"bearer",
                "expires_in":1209599,
                "userName":"PUBLIC_KEY",
                ".issued":"Fri, 07 Jul 2017 16:47:46 GMT",
                ".expires":"Fri, 21 Jul 2017 16:47:46 GMT"
            }

        """
        response = requests.post(
            BearerAuth.TOKEN_URL,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"},
            data=(f"grant_type=client_credentials"
                  f"&client_id={public_key}&"
                  f"client_secret={private_key}")
        )
        
        return response.json()


    def get_expiration_str(self):
        return self.expires.strftime(BearerAuth.EXPIRATION_FORMAT_STR)
