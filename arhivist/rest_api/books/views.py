# coding: utf-8
"""
Views for books-rest-api.
"""
import json

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from books.models import (
    Book, Category
)
from rest_api import StandardResultsSetPagination
from .serializers import BookSerializer

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


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
        cat_id = self.request.query_params.get('cat_id', None)
        if cat_id is not None:
            cat = Category.objects.get(pk=cat_id)
            queryset = Book.objects.filter(categories=cat).order_by("title")
        return queryset

    # __POST-methods

    def post(self, request, *args, **kwargs):
        try:
            json_payload = json.loads(request.POST["books"])
            owner = User.objects.get(pk=request.user.pk)
            for data in json_payload:
                book = Book.from_request(owner, data)
                serializer = BookSerializer(book)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, book_id):
        page_num = request.GET.get("page", 1)
        cats = Category.objects.all().order_by("name")
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise Http404
        return render(request, "book.html", {"cats": cats, "book": book, "pn": page_num})


