"""
Books app tests.
"""
import json
import requests

from arhivist.api.settings import *
from arhivist.parser.item import Book

with open("test.json", "r") as inp:
    test_data = json.load(inp)

# ------------------
# Low-level requests
# ------------------

def test_get_books():
    resp_json = requests.get(url=BOOKS_URL).json()
    assert resp_json


def test_unauthorized_post():
    resp = requests.post(url=BOOKS_URL)
    assert resp.status_code == requests.status_codes.codes.unauthorized


def test_authorized_post(ArhClient):
    data_json = test_data["1"]["req"]
    resp = requests.post(url=BOOKS_URL, json=data_json, headers=ArhClient.token_header)

    assert resp.status_code == requests.status_codes.codes.created
    assert len(data_json["books"]) == len(resp.json())


def test_post_single_book(ArhClient):
    book_json = test_data["2"]["req"]
    resp = requests.post(url=BOOKS_URL, json=book_json, headers=ArhClient.token_header)
    assert resp.status_code == requests.status_codes.codes.created

# ------------------
# Arhivist client
# ------------------

def test_client_post(ArhClient):
    data_json = test_data["1"]["req"]["books"][0]
    book = Book.from_json(data_json)
    resp = ArhClient.post_book(book)
    assert resp.status_code == requests.status_codes.codes.created