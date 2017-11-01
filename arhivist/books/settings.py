# coding: utf-8
import re

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


# __FOLDER
STORE_PATH = '/home/vladworld/books'
UNCHECKABLE_FOLDERS = ()

# __FILES
SUPPORT_TYPES = {'pdf', 'djvu', '.djv', 'epub', 'fb2'}
BOOK_NAME_MASK = re.compile(r'(?P<name>\w+)\.(?P<type>\w+)')
UNICODE_NAME_MASK = lambda f: re.findall(r'(?u)\w+', f)

# __URLS
POST_URL = 'http://127.0.0.1:8000/books/'
