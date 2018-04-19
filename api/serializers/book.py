from rest_framework import serializers

from catalogue.models import Book

from .category import CategorySerializer


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.full_name')
    publisher = serializers.CharField(source='publisher.title')
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'category', 'publisher')
