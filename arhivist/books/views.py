# coding: utf-8
"""
Books-app views.
"""
import random

from django.views.generic import ListView, DetailView, TemplateView

from .models import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


def random_book():
    number_of_records = Book.objects.count()
    random_index = int(random.random() * number_of_records) + 1
    return Book.objects.get(pk=random_index)


class BooksList(ListView):

    queryset = Book.objects.all()
    template_name = "index.html"
    paginate_by = 3
    cat = None

    def get(self, request, *args, **kw):
        cat_id = self.kwargs["cat_id"]
        if cat_id:
            self.cat = Category.objects.get(pk=cat_id)
        return super().get(request, *args, **kw)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cats"] = Category.objects.order_by("name")
        context["category"] = self.cat
        context["random_book"] = random_book()
        return context

    def get_queryset(self):
        if self.cat:
            return Book.objects.filter(category=self.cat).order_by("title")
        else:
            return Book.objects.all().order_by("title")


class BookDetail(DetailView):

    template_name = "book.html"
    model = Book
    pk_url_kwarg = "book_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pn"] = self.request.GET.get("page", "1")
        context["cats"] = Category.objects.order_by("name")
        context["random_book"] = random_book()
        return context


class CategoryList(ListView):

    queryset = Category.objects.all().order_by("name")
    template_name = "category.html"
    paginate_by = 10
