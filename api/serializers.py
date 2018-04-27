from django.db.models import Count, Q
from django.contrib.auth.models import User
from rest_framework import serializers

from catalogue import models


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Author
        fields = ('id', 'last_name', 'first_name', 'full_name', )


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='title')

    class Meta:
        model = models.Category
        fields = ('id', 'category', )


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields = ('id', 'title', 'author', 'category', 'publisher')


class BookForPublisherSerializer(BookSerializer):
    author = serializers.CharField(source='author.full_name')
    publisher = serializers.CharField(source='publisher.title')
    category = CategorySerializer()

    class Meta(BookSerializer.Meta):
        model = models.Book


class PublisherSerializer(serializers.ModelSerializer):
    books = BookForPublisherSerializer(many=True, read_only=True)

    class Meta:
        model = models.Publisher
        fields = ('id', 'title', 'books')


class BookmarkSerializer(serializers.ModelSerializer):
    in_bookmarks = serializers.BooleanField()
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Bookmark
        fields = ('id', 'user', 'user_name', 'book', 'in_bookmarks', )


class BookmarkUserSerializer(BookmarkSerializer):
    user = serializers.ReadOnlyField(source='user.id')


class UserAdminSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkUserSerializer(many=True, read_only=True)
    bookmark_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'bookmarks', 'bookmark_amount', )

    def get_bookmark_amount(self, obj):
        return models.Bookmark.objects.filter(user=obj.id, in_bookmarks=True).count()


class UserRestrictedSerializer(UserAdminSerializer):
    user_name = serializers.ReadOnlyField(source='username')

    class Meta(UserAdminSerializer):
        model = User
        fields = ('id', 'user_name', 'bookmarks', 'bookmark_amount', )
