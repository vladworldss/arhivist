# coding: utf-8
"""
API-app views.
"""
import json

from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from books.models import Book, Category
from api.pagination import StandardResultsSetPagination
from .serializers import BookSerializer, CategorySerializer

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"
__all__        = ("BooksList", "BookDetail", "CategoryList", "BookSearch")


class BooksList(ListCreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = StandardResultsSetPagination

    # __GET-methods

    def get_queryset(self):
        """
        Overwrite for custom filtering.
        :return:
        """
        queryset = Book.objects.all()
        cat_id = self.kwargs.get('cat_id', None)
        if cat_id is not None:
            try:
                cat = Category.objects.get(pk=cat_id)
                queryset = Book.objects.filter(category=cat).order_by("title")
            except Category.DoesNotExist:
                raise Http404
        return queryset

    # __POST-methods

    def post(self, request, *args, **kwargs):
        try:
            json_data = request.data
            if isinstance(json_data, str):
                json_data = json.loads(json_data)

            json_payload = json_data["books"]
            owner = User.objects.get(pk=request.user.pk)
            result = []
            if not isinstance(json_payload, (list, tuple)):
                json_payload = (json_payload, )
            for data in json_payload:
                data["owner"] = owner
                book = Book.from_request(data)
                serializer = BookSerializer(book)
                result.append(serializer.data)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetail(RetrieveUpdateDestroyAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class BookSearch(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = "raw_title"

    def get_queryset(self):
        book_title = self.kwargs.get(self.lookup_field)
        book = Book.objects.filter(raw_title=book_title)
        return book


class CategoryList(ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = StandardResultsSetPagination
