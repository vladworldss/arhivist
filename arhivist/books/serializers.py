# coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers

from books.models import Book

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class BookSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = ('publisher', 'description', 'language',
                  'published_date', 'title', 'page_count',
                  'canonical_volume_link', 'isbn_10', 'isbn_13',
                  'authors', 'categories', 'raw_title', 'path',
                  'validate', 'file_ext', 'owner'
                  )


class UserSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'books')
