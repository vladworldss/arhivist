# coding: utf-8
"""
Books-app views.
"""
from django.views.generic import ListView, DetailView

from .models import *

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class BooksList(ListView):

    queryset = Book.objects.all()
    template_name = "index.html"
    paginate_by = 10
    cat = None

    def get(self, request, *args, **kw):
        cat_id = self.kwargs["cat_id"]
        if cat_id is None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk = cat_id)
        return super().get(request, *args, **kw)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cats"] = Category.objects.order_by("name")
        context["category"] = self.cat
        return context

    def get_queryset(self):
        return Book.objects.filter(category=self.cat).order_by("title")


class BookDetail(DetailView):

    template_name = "book.html"
    model = Book
    pk_url_kwarg = "book_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pn"] = self.request.GET.get("page", "1")
        context["cats"] = Category.objects.order_by("name")
        return context
