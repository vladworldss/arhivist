# coding: utf-8
"""
Books-app models.
"""
from django.db import models
from django.core.exceptions import FieldError

__author__     = "Vladimir Gerasimenko"
__copyright__  = "Copyright (C) 2017, Vladimir Gerasimenko"
__version__    = "0.0.1"
__maintainer__ = "Vladimir Gerasimenko"
__email__      = "vladworldss@yandex.ru"


class CustomModel(object):

    @classmethod
    def make(cls, *args, **kw):
        inst, created = cls.objects.get_or_create(*args, **kw)
        return inst


class Publisher(models.Model, CustomModel):
    name = models.CharField(max_length=30, blank=True, default='')
    address = models.CharField(max_length=50, blank=True, default='')
    city = models.CharField(max_length=60, blank=True, default='')
    state_province = models.CharField(max_length=30, blank=True, default='')
    country = models.CharField(max_length=50, blank=True, default='')
    website = models.URLField(blank=True, default='')

    class Meta:
        ordering = ("name", )
        verbose_name = "издательство"
        verbose_name_plural = "издательства"
        unique_together = ("name", "city", "address")

    def __str__(self):
        return self.name


class Author(models.Model, CustomModel):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40, blank=True, default='')
    email = models.EmailField(blank=True, default='')

    def __str__(self):
        return "{} {}".format(self.name, self.surname)

    class Meta:
        ordering = ("name", "surname")
        verbose_name = "автор"
        verbose_name_plural = "авторы"
        unique_together = ("name", "surname")


class Language(models.Model, CustomModel):
    name = models.CharField(max_length=3, unique=True)

    class Meta:
        ordering = ("name", )
        verbose_name = "язык"
        verbose_name_plural = "языки"

    def __str__(self):
        return self.name


class Category(models.Model, CustomModel):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ("name", )
        verbose_name = "категория"
        verbose_name_plural = "категории"
        unique_together = ("name", )


class Book(models.Model, CustomModel):
    publisher = models.ForeignKey(Publisher, null=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    language = models.ForeignKey(Language)
    published_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=128)
    page_count = models.IntegerField(default=0)
    volume_link = models.URLField()
    isbn_10 = models.IntegerField(unique=True, blank=True, null=True)
    isbn_13 = models.IntegerField(unique=True, blank=True, null=True)
    author = models.ManyToManyField(Author)
    category = models.ManyToManyField(Category)
    thumbnail = models.CharField(max_length=128)

    # Service data
    path = models.FilePathField(blank=True, null=True)
    raw_title = models.CharField(max_length=128)
    file_ext = models.CharField(max_length=8, default='')
    validate = models.BooleanField(default=False, db_index=True)

    # Auth data
    owner = models.ForeignKey('auth.User', related_name='books', on_delete=models.CASCADE)

    class Meta:
        ordering = ("title", )
        verbose_name = "книга"
        verbose_name_plural = "книги"
        unique_together = ("title", "raw_title", "file_ext")

    def __str__(self):
        authors = ', '.join([x.name for x in self.author.all()])
        return '{}. {}.{}'.format(authors, self.title, self.file_ext)

    @staticmethod
    def from_request(data):
        def add_foreign(inst, ModelCls, name):
            """
            Add to instance foreign relations.

            :param models.Model inst:
            :param type ModelCls:
            :param iter-obj names:
            :return: updated inst
            """
            foreign_inst = ModelCls.make(name=name)
            foreign_field_name = ModelCls.__name__.lower()
            foreign_field = getattr(inst, foreign_field_name)
            foreign_field.add(foreign_inst)

        author_names = data.pop("author")
        category_names = data.pop("category")

        data["publisher"] = Publisher.make(name=data["publisher"])
        data["language"] = Language.make(name=data["language"])
        book = Book.make(**data)
        [add_foreign(book, Author, x) for x in author_names]
        [add_foreign(book, Category, x) for x in category_names]
        book.save()
        return book
