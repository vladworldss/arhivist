# coding: utf-8
"""
Json-serializers for books-rest-api.
"""

from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField
)

from books.models import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class BookSerializer(ModelSerializer):
    """
    Book serializer class.
    """

    owner = ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    """
    Book serializer class.
    """

    owner = ReadOnlyField(source='owner.username')

    class Meta:
        model = Category
        fields = "__all__"
