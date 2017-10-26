# coding: utf-8
from django.db import models


def _make(cls, *args, **kw):
    inst = None
    try:
        inst = cls.objects.get(name=kw.get('name'))
    except cls.DoesNotExist:
        inst = cls(*args, **kw)
        inst.save()
    return inst


class Publisher(models.Model):
    name = models.CharField(max_length=30, blank=True, default='')
    address = models.CharField(max_length=50, blank=True, default='')
    city = models.CharField(max_length=60, blank=True, default='')
    state_province = models.CharField(max_length=30, blank=True, default='')
    country = models.CharField(max_length=50, blank=True, default='')
    website = models.URLField(blank=True, default='')

    class Meta:
        ordering = ["name"]
        verbose_name = "издательство"
        verbose_name_plural = "издательства"
        unique_together = ("name", "city", "address")

    def __str__(self):
        return self.name

    @classmethod
    def make(cls, *args, **kw):
        return _make(cls, *args, **kw)


class Author(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=40, blank=True, default='')
    email = models.EmailField(blank=True, default='')

    def __str__(self):
        return "{} {}".format(self.name, self.surname)

    class Meta:
        ordering = ["name", "surname"]
        verbose_name = "автор"
        verbose_name_plural = "авторы"
        unique_together = ("name", "surname")

    @classmethod
    def make(cls, *args, **kw):
        return _make(cls, *args, **kw)


class Language(models.Model):
    name = models.CharField(max_length=3, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "язык"
        verbose_name_plural = "языки"

    def __str__(self):
        return self.name

    @classmethod
    def make(cls, *args, **kw):
        return _make(cls, *args, **kw)


class Categories(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "категория"
        verbose_name_plural = "категории"

    @classmethod
    def make(cls, *args, **kw):
        return _make(cls, *args, **kw)


class Book(models.Model):
    publisher = models.ForeignKey(Publisher, null=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    language = models.ForeignKey(Language)
    published_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=128)
    page_count = models.IntegerField(default=0)
    canonical_volume_link = models.URLField()
    isbn_10 = models.IntegerField(unique=True, blank=True, null=True)
    isbn_13 = models.IntegerField(unique=True, blank=True, null=True)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Categories)

    # Service data
    path = models.FilePathField(blank=True, null=True)
    raw_title = models.CharField(max_length=128)
    file_ext = models.CharField(max_length=8, default='')
    validate = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["title"]
        unique_together = ["title", "path", "raw_title", "file_ext"]
        verbose_name = "книга"
        verbose_name_plural = "книги"

    def __str__(self):
        authors = ', '.join([x.name for x in self.authors.all()])
        return '{}. {}.{}'.format(authors, self.title, self.file_ext)

    @classmethod
    def make(cls, *args, **kw):
        inst = None
        try:
            conf = {}
            for x in ["title", "path", "raw_title", "file_ext"]:
                conf[x] = kw.get(x, '')
            inst = cls.objects.get(**conf)
        except cls.DoesNotExist:
            inst = cls(*args, **kw)
            inst.save()
        return inst
