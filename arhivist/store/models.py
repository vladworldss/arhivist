from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=128)


class Book(models.Model):
    publisher = models.TextField()
    description = models.TextField(max_length=256)
    language = models.CharField(max_length=16)
    publishedDate = models.DateTimeField()
    title = models.CharField(max_length=128)
    pageCount = models.IntegerField()
    canonicalVolumeLink = models.URLField()
    isbn_10 = models.IntegerField()
    isbn_13 = models.IntegerField()
    author = models.ForeignKey(Author)
