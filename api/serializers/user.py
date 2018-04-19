from django.contrib.auth.models import User
from rest_framework import serializers

from .bookhighlight import BookHighlightSerializer


class BookHighlightForUserSerializer(BookHighlightSerializer):
    class Meta(BookHighlightSerializer.Meta):
        fields = ('id', 'book', 'in_bookmarks', )


class UserSerializer(serializers.ModelSerializer):
    highlights = BookHighlightForUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'highlights', )
