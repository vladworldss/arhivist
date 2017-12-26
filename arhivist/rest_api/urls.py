# coding: utf-8
"""
URL's for rest-api-app.
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.response import Response

from rest_api.books import BooksList, BookDetail
from .user import CreateUserView

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


urlpatterns = [
    url(r'^auth/', obtain_jwt_token),
    url(r'^books/(?:(?P<cat_id>\d+)/)?$', BooksList.as_view(), name="api-books"),

    url(r'^book/(?P<book_id>\d+)/$', BookDetail.as_view(), name='api-book'),
    url('^register/$', CreateUserView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
