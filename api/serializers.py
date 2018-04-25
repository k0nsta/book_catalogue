from django.db.models import Count, Q
from django.contrib.auth.models import User
from rest_framework import serializers

from catalogue.models import Book
from catalogue.models import Author
from catalogue.models import Publisher
from catalogue.models import Category
from catalogue.models import Bookmark


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'last_name', 'first_name', 'full_name', )


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='title')

    class Meta:
        model = Category
        fields = ('id', 'category', )


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.full_name')
    publisher = serializers.CharField(source='publisher.title')
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'category', 'publisher')


class BookForPublisherSerializer(BookSerializer):
    publisher = None

    class Meta(BookSerializer.Meta):
        model = Book


class PublisherSerializer(serializers.ModelSerializer):
    books = BookForPublisherSerializer(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ('id', 'title', 'books')


class BookmarkSerializer(serializers.ModelSerializer):
    in_bookmarks = serializers.BooleanField()

    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'book', 'in_bookmarks', )


class BookmarkUserSerializer(BookmarkSerializer):
    user = serializers.CharField(source='user.id', read_only=True)

    class Meta(BookmarkSerializer.Meta):
        fields = ('id', 'book', 'in_bookmarks', )


class UserSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkUserSerializer(many=True, read_only=True)
    bookmark_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'bookmarks', 'bookmark_amount', )

    def get_bookmark_amount(self, obj):
        print(Bookmark.objects.filter(user=obj.id, in_bookmarks=True).count())
        return Bookmark.objects.filter(user=obj.id, in_bookmarks=True).count()
