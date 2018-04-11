# coding: utf-8
"""
Arhivist REST-API settings.
"""

VENDORS = ["google"]

# __URLS
LOCAL_URL = "http://127.0.0.1:8000/"
API_URL = LOCAL_URL + "api/"
AUTH_URL = API_URL + 'auth/'
BOOKS_URL = API_URL + 'books/'
BOOK_URL = BOOKS_URL + 'book/'

CREDENTIALS = {'username': 'admin', 'password': 'admin123123'}
