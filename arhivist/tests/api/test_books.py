"""
Tests /api/books
"""
import json
import pytest
import requests


with open("test.json", "r") as inp:
    test_data = json.load(inp)

API_BOOKS_URL = "http://127.0.0.1:8000/api/books/"
API_AUTH_URL = "http://127.0.0.1:8000/api/auth/"
CREDENTIALS = {'username':'admin', 'password':'admin123123'}


def test_get_books():
    resp_json = requests.get(url=API_BOOKS_URL).json()
    assert resp_json


def test_post_books():
    non_auth_resp = {'detail': 'Authentication credentials were not provided.'}
    resp =requests.post(url=API_BOOKS_URL).json()
    assert non_auth_resp == resp

    resp_json = requests.post(url=API_AUTH_URL, data=CREDENTIALS).json()
    token = resp_json["token"]
    data_json = json.dumps(test_data["1"]["req"])
    payload = {"books": data_json}
    resp = requests.post(url=API_BOOKS_URL, data=payload, headers={'Authorization': f'JWT {token}'})