# coding: utf-8
"""
Модуль настроек parser
"""
import re

# __FOLDER

BASE_PATH = '/home/vladworld/books'

UNCHECKABLE_FOLDERS = ()

# __FILES

SUPPORT_TYPES = {'pdf', 'djvu', '.djv', 'epub', 'fb2'}

BOOK_NAME_MASK = re.compile(r'(?P<name>\w+)\.(?P<type>\w+)')

UNICODE_NAME_MASK = lambda f: re.findall(r'(?u)\w+', f)
