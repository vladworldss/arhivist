# coding: utf-8
import pytest

# from arhivist.parser.store import Store
from arhivist.parser.api.google import Book

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
#regex = re.compile(r"http://[\w\./]*\?id=(?P<id>\w+)&\w+")



thumbnail_url = 'http://books.google.com/books/content?id=gNFcTw52DPUC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'
dest = '/home/vladworldss/PycharmProjects/arhivist/arhivist/parser/test_thumb.png'
resp = Book.get_thumbnail(thumbnail_url)
Book.save_thumbnail(resp, dest)
