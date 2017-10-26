# coding: utf-8
import pytest

from .store import Store

def test_conf(publisher, language):
    return {'publisher': publisher,
            'description': '',
            'language': language,
            'published_date': '2005-01-01',
            'title': 'How to Live Like You Were Dying- PDF',
            'page_count': '0',
            'canonical_volume_link': 'https://books.google.com/books/about/How_to_Live_Like_You_Were_Dying_PDF.html?hl=&id=gNFcTw52DPUC',
            'path': '/home/test/',
            'raw_title': 'xxx'
            }