from django_filters import rest_framework as filters

from catalogue import models


class BookTitleFilter(filters.FilterSet):
    class Meta:
        model = models.Book
        fields = {
            'title': ['icontains', 'exact', ],
        }
