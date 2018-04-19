from rest_framework import serializers

from .book import BookSerializer

from catalogue.models import BookHighlight


class BookHighlightSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    book = BookSerializer()
    in_bookmarks = serializers.BooleanField()

    class Meta:
        model = BookHighlight
        fields = ('id', 'user', 'book', 'in_bookmarks', )
