# coding: utf-8
"""
Module for api tests
"""
import sys
sys.dont_write_bytecode = True

import pytest


@pytest.fixture(scope='module')
def Api():
    class _Api:
        from .google import Api
        _self = Api()
        list = _self.list
    return _Api


def test_google_req(Api):
    import json

    title = lambda f: f['items'][0]['volumeInfo']['title']

    with open('test_response.json', 'r') as resp:
        t = json.load(resp)
        test_title = title(t)
        assert title(Api.list('isbn:0596007973')) == test_title
