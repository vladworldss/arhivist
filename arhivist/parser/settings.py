# coding: utf-8
"""
Module of Parser settings.
"""
import os

from arhivist import books
from arhivist.api.settings import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.3"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"

# __FOLDER
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STORE_PATH = "/home/test/books/"
UNCHECKABLE_FOLDERS = ()
SUPPORT_BOOK_EXTENSION = {'pdf', 'djvu', '.djv', 'epub', 'fb2'}

# __URLS
AUTH_URL = AUTH_URL
CREDENTIALS = CREDENTIALS
POST_URL = BOOKS_URL

# __THUMBNAIL
BOOKS_DIR = os.path.join(PROJECT_DIR, "books")
THUMBNAIL_DIR = os.path.join(BOOKS_DIR, "static", "thumbnail")
