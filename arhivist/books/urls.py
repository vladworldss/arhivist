# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from books.views import BooksList, UserList

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


urlpatterns = [
    url(r'^books/$', BooksList.as_view()),
    url(r'^users/$', UserList.as_view()),

    # url(r'^books/(?P<pk>[0-9]+)/$', views.books_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)

