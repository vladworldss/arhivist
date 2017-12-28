# coding: utf-8
"""
URL's for rest-api-app.
"""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.response import Response

from api.books import *
from .user import CreateUserView

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


urlpatterns = [
    url(r'^auth/', obtain_jwt_token),
    url('^register/$', CreateUserView.as_view()),

    url(r'^books/(?:(?P<cat_id>\d+)/)?$', BooksList.as_view(), name="api-books"),
    url(r'^books/book/(?P<pk>\d+)/$', BookDetail.as_view(), name='api-book'),
    url(r'^books/category/$', CategoryList.as_view(), name='api-category'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
