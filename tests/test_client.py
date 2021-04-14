# Python imports
import json, os, sys

# NOTE: Ensures that the code directory is in the python system path 
# for the internal imports below
code_directory = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
if code_directory not in sys.path:
    sys.path.append(code_directory)

# Internal imports
from tcgplayer_api.auth import BearerAuth
from tcgplayer_api.client import TCGPlayerClient


CREDENTIAL_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "tcg_player_credentials.json"))


def generate_client():
    with open(CREDENTIAL_FILE_PATH, "r") as fs:
        credentials = json.load(fs)

    if credentials:
        if 'public_key' not in credentials:
            raise KeyError(f"'public_key' not found in credential file @ {CREDENTIAL_FILE_PATH}")
        elif 'private_key' not in credentials:
            raise KeyError(f"'private_key' not found in credential file @ {CREDENTIAL_FILE_PATH}")
        auth_cred = {
            'public_key': credentials["public_key"],
            'private_key': credentials["private_key"],
        }
        if 'token' in credentials:
            auth_cred['token'] = credentials['token']
            if 'expires' in credentials:
                auth_cred['token_expiration'] = credentials['expires']
        auth = BearerAuth(**auth_cred)
        client = TCGPlayerClient(auth=auth)
        return client
    else:
        raise ValueError(f"No Credential file found @ {CREDENTIAL_FILE_PATH}")
    
    return None


def check_api_response(response, total_items=None):
    assert type(response) == dict
    
    has_total_items = False
    if total_items is None:
        if 'totalItems' in response:
            has_total_items = True
            assert type(response['totalItems']) == int
    elif total_items:
        has_total_items = True
        assert "totalItems" in response
        assert type(response['totalItems']) == int
    
    assert "success" in response
    assert type(response["success"]) == bool
    assert response['success']
    assert "results" in response
    assert type(response["results"]) == list
    
    if has_total_items:
        assert len(response["results"]) == response["totalItems"]


def list_all_categories_test(client):
    response = client.list_all_categories()
    check_api_response(response)


def test_client_basic():
    client = generate_client()
    
    list_all_categories_test(client)

