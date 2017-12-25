# coding: utf-8
"""
Parser tests.
"""
import os
import json
from arhivist.tests.conftest import *
from arhivist.parser.executor import BookExecutor


@pytest.mark.parametrize("book", ["test.djvu", "test.pdf", "test.epub", "test.fb2"])
def test_get_meta(api, book):
    assert api.get_meta(book)


def test_thumbnail_dir(GoogleApi, capsys):
    with capsys.disabled():
        print(GoogleApi.download_dir)
    assert GoogleApi.download_dir == "/home/vladworldss/PycharmProjects/arhivist/arhivist/books/static/thumbnail"


def test_execute_without_callback(books, GoogleApi):
    BookExecutor.execute(books, 'google', callback=False)
    pngs = set((x for x in os.listdir(GoogleApi.download_dir) if x.endswith('.png')))
    pngs.remove('test_thumb.png')
    assert pngs
