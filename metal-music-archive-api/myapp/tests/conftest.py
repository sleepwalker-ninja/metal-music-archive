import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from ninja_jwt.tokens import RefreshToken

# User = get_user_model()

# @pytest.fixture
# def user(db):
#     return User.objects.create_user(username="James", password="DaveIsGoat")

# @pytest.fixture
# def client():
#     return Client()

# @pytest.fixture
# def login_response(client, user):
#     response = client.post(
#         "/api/token/pair",
#         data={
#             "username": user.username,
#             "password": "DaveIsGoat"
#         },
#         content_type="application/json"
#     )
    
#     return response

# @pytest.fixture
# def access_token(login_response):
#     if login_response.status_code != 200:
#         print(f"Login failed: {login_response.content}") # This will show in 'Captured stdout setup'
#     assert login_response.status_code == 200
#     data = login_response.json()
#     return data["access"]

# @pytest.fixture
# def auth_client(client, access_token):
#     client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
#     return client


""" 
access_token
 └── login_response
      ├── client
      └── user
           └── db

"""


# User = get_user_model()

# @pytest.fixture
# def user(db):
#     user = User.objects.create(
#         username = "James",
#         password = "GoatDave"
#     )
#     return user

# @pytest.fixture
# def client():
#     return Client()

# def login_response(client, user):
#     response = client.post(
#         "/api/token/pair",
#         data = {
#             "username": user.username,
#             "password": "GoatDave"
#         },
#         content_type = "application/json"
#     )
#     return response

# @pytest.fixture
# def access_toke(login_response):
#     data = login_response.json()
#     return data["access"]



User = get_user_model()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username = "James",
        password = "GoatDave"
    )
    
    return user

@pytest.fixture
def auth_client(client, test_user):
    refresh = RefreshToken.for_user(test_user)
    access_token = str(refresh.access_token)
    
    class AuthenticatedClient:
        def __init__(self, client, token):
            self.client = client
            self.header = f"Bearer {token}"

        def get(self, path, **kwargs):
            return self.client.get(path, HTTP_AUTHORIZATION=self.header, **kwargs)

        def post(self, path, data=None, content_type="application/json", **kwargs):
            return self.client.post(
                path, 
                data=data, 
                content_type=content_type, 
                HTTP_AUTHORIZATION=self.header, 
                **kwargs
            )
            
        def patch(self, path, data=None, content_type="application/json", **kwargs):
            return self.client.patch(
                path, 
                data=data,
                content_type=content_type,
                HTTP_AUTHORIZATION=self.header,
                **kwargs
            )
            
        def delete(self, path, **kwargs):
            return self.client.delete(
                path, 
                HTTP_AUTHORIZATION=self.header,
                **kwargs
            )

    return AuthenticatedClient(client, access_token)

import pytest
import requests


BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def api_base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_header():
    payload = {
        "username": "Dave",
        "password": "diana"
    }
    
    response = requests.post(f"{BASE_URL}/api/token/pair", json=payload)
    if response.status_code == 200:
        token = response.json().get("access")
        return {"Authorization": f"Bearer {token}"}
    else: 
        pytest.fail("Failed to obtain auth token")


