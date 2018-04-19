from django.db import models

from .behaviors import Timestampable
from .behaviors import Isactiveable
from .behaviors import Titleable
from .behaviors import IsVoidable


# Create your models here.
class Author(Isactiveable, Timestampable, IsVoidable, models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    class Meta:
        default_related_name = 'authors'

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Publisher(Titleable, Isactiveable, Timestampable, IsVoidable, models.Model):

    class Meta:
        default_related_name = 'publishers'

    def __str__(self):
        return self.title


class Category(Titleable, Isactiveable, Timestampable, IsVoidable, models.Model):

    class Meta:
        default_related_name = 'categories'

    def __str__(self):
        return self.title


class Book(Titleable, Isactiveable, Timestampable, IsVoidable, models.Model):
    author = models.ForeignKey(Author, models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, models.CASCADE, blank=True, null=True)
    publisher = models.ForeignKey(Publisher, models.CASCADE, blank=True, null=True)

    class Meta:
        default_related_name = 'books'

    def __str__(self):
        return self.title


