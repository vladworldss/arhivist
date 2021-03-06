# coding: utf-8
"""
Books-app URL Configuration.
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from books.views import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


urlpatterns = [
    url(r'^(?:(?P<cat_id>\d+)/)?$', BooksList.as_view(), name='index'),
    url(r'^book/(?P<book_id>\d+)/$', BookDetail.as_view(), name='book'),
    url(r'^сategories/$', CategoryList.as_view(), name="сategories")
]

urlpatterns = format_suffix_patterns(urlpatterns)
