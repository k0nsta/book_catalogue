from rest_framework import serializers

from catalogue.models import Publisher

from .book import BookForPublisherSerializer


class PublisherSerializer(serializers.ModelSerializer):

    books = BookForPublisherSerializer(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ('id', 'title', 'books')
