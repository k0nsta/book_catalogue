from django.db.models import Count, Q
from django.contrib.auth.models import User
from rest_framework import serializers

from catalogue.models import Book
from catalogue.models import Author
from catalogue.models import Publisher
from catalogue.models import Category
from catalogue.models import Bookmark


# Author serialaziers
# =================================================================================
class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'last_name', 'first_name', 'full_name', )


# Category serialaziers
# =================================================================================
class CategorySerializer(serializers.ModelSerializer):
    """
    Implemented field's serialization. Serializer fields
    handle converting between primitive values and internal datatypes.
    They also deal with validating input values, as well as retrieving
    and setting the values from their parent objects.
    See: http://www.django-rest-framework.org/api-guide/fields/
    """
    category = serializers.CharField(source='title')

    class Meta:
        model = Category
        fields = ('id', 'category', )


# Book serialaziers
# =================================================================================
class BookSerializer(serializers.ModelSerializer):
    """
    Implemented several different technics for cilent-side view data.
    1:The model 'Author' doesn't have a field 'full name',
    it has fields 'first_name', 'last_name'. Full name has been
    converted on model side, used by @property. On client side
    represent like str.
    2: We redeclarate publisher's field 'title' on 'publisher' used by
    field serialization inside 'BookSerializer', other ways we can get
    on client-side publisher's filed name is 'title'.
    """
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


# Publisher serialaziers
# =================================================================================
class PublisherSerializer(serializers.ModelSerializer):
    """
    Implemented fields option. The 'fields' options allow explicitly
    set all fields that should be serialized.
    See: http://www.django-rest-framework.org/api-guide/serializers/#specifying-which-fields-to-include
    """
    books = BookForPublisherSerializer(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ('id', 'title', 'books')


# BookHighlight serialaziers
# =================================================================================
class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.id', read_only=True)
    in_bookmarks = serializers.BooleanField()

    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'book', 'in_bookmarks', )


class BookHighlightForUserSerializer(BookmarkSerializer):
    class Meta(BookmarkSerializer.Meta):
        fields = ('id', 'book', 'in_bookmarks', )


# User serialaziers
# =================================================================================
class UserSerializer(serializers.ModelSerializer):
    bookmarks = BookHighlightForUserSerializer(many=True, read_only=True)
    bookmark_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'bookmarks', 'bookmark_amount', )

    def get_bookmark_amount(self, obj):
        print(Bookmark.objects.filter(user=obj.id, in_bookmarks=True).count())
        return Bookmark.objects.filter(user=obj.id, in_bookmarks=True).count()
