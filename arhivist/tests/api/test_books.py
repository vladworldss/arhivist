"""
Tests /api/books
"""
import json
from tests.conftest import *

with open("test.json", "r") as inp:
    test_data = json.load(inp)


def test_get_books():
    resp_json = requests.get(url=BOOKS_URL).json()
    assert resp_json


def test_unauthorized_post():
    resp = requests.post(url=BOOKS_URL)
    assert resp.status_code == requests.status_codes.codes.unauthorized


def test_authorized_post(token):
    data_json = test_data["1"]["req"]
    resp = requests.post(url=BOOKS_URL, json=data_json, headers={'Authorization': f'JWT {token}'})

    assert resp.status_code == requests.status_codes.codes.created
    assert len(data_json["books"]) == len(resp.json())
