# coding: utf-8
import json
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render
from django.http import Http404

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from books.models import *
from books.serializers import BookSerializer, UserSerializer

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class BooksList(generics.ListCreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def update_post_request(self, request, **kw):
        request.POST._mutable = True
        for key, value in kw.items():
            if key in request.POST:
                request.POST[key] = value

    def get_values_from_request(self, request, model_name):
        vals = request.POST.getlist(model_name)
        request.POST.pop(model_name)
        return vals

    def get(self, request, cat_id):
        page_num = request.GET.get('page', 1)
        cats = Categories.objects.all().order_by("name")
        if cat_id is None:
            cat = Categories.objects.first()
        else:
            cat = Categories.objects.get(pk=cat_id)
        paginator = Paginator(Book.objects.filter(categories=cat).order_by("title"), 10)

        try:
            books = paginator.page(page_num)
        except InvalidPage:
            books = paginator.page(1)
        return render(request, "index.html", {"category": cat, "cats": cats, "books": books})

    def post(self, request, *args, **kwargs):
        """
        List all books, or create a new book.
        """
        try:
            publisher = Publisher.make(name=request.POST['publisher'])
            language = Language.make(name=request.POST['language'])
            self.update_post_request(request, publisher=publisher, language=language)
            authors_names = self.get_values_from_request(request, 'authors')
            categories_names = self.get_values_from_request(request, 'categories')
            owner = User.objects.get(pk=request.user.pk)
            request.POST.update({'owner':owner})
            try:
                book = Book.make(**request.POST.dict())
                for a in authors_names:
                    auth = Author.make(name=a)
                    book.authors.add(auth)

                for c in categories_names:
                    cat = Categories.make(name=c)
                    book.categories.add(cat)
                book.save()

            except Exception as e:
                return Response(str(e))

            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, book_id):
        cats = Categories.objects.all().order_by("name")
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise Http404(f'Book does not exist')
        return render(request, "book.html", {"cats": cats, "book": book})


class UserList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
