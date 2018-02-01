# coding: utf-8
import os

from arhivist import books

from arhivist.api.settings import AUTH_URL, BOOKS_URL, CREDENTIALS

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


# __FOLDER
STORE_PATH = '/home/test/books'
UNCHECKABLE_FOLDERS = ()
SUPPORT_BOOK_EXTENSION = {'pdf', 'djvu', '.djv', 'epub', 'fb2'}

# __VENDORS
vendors = ["google"]

# __URLS
AUTH_URL = AUTH_URL
CREDENTIALS = CREDENTIALS
POST_URL = BOOKS_URL

# __THUMBNAIL
BOOKS_DIR = os.path.abspath(books.__path__[-1])
THUMBNAIL_DIR = os.path.join(BOOKS_DIR, "static", "thumbnail")
