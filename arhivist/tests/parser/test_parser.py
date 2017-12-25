# coding: utf-8
"""
Parser tests.
"""
import os
import json
import sys
sys.dont_write_bytecode = True
from arhivist.tests.conftest import *
# from arhivist.parser.executor import BookExecutor
from . import exiftool

# @pytest.mark.parametrize("book", ["test.djvu", "test.pdf", "test.epub", "test.fb2"])
@pytest.mark.parametrize("book", ["test.djvu"])
def test_get_meta(book, capsys):
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(book)
    with capsys.disabled():
        print()
        print(metadata["DjVu:Title"])
        print(metadata["DjVu:Author"])
    # assert api.get_meta(book)


# def test_thumbnail_dir(GoogleApi, capsys):
#     with capsys.disabled():
#         print(GoogleApi.download_dir)
#     assert GoogleApi.download_dir == "/home/vladworldss/PycharmProjects/arhivist/arhivist/books/static/thumbnail"
#
#
# def test_execute_without_callback(books, GoogleApi):
#     BookExecutor.execute(books, 'google', callback=False)
#     pngs = set((x for x in os.listdir(GoogleApi.download_dir) if x.endswith('.png')))
#     pngs.remove('test_thumb.png')
#     assert pngs
