from django.contrib.auth.models import User
from rest_framework import serializers

from catalogue.models import Book
from catalogue.models import Author
from catalogue.models import Publisher
from catalogue.models import Category
from catalogue.models import BookHighlight


# Author serialaziers
# =================================================================================
class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'full_name', )


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
    create = serializers.CharField(source='create_date')

    class Meta:
        model = Category
        fields = ('id', 'category', 'create')


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
class BookHighlightSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    book = BookSerializer()
    in_bookmarks = serializers.BooleanField()

    class Meta:
        model = BookHighlight
        fields = ('id', 'user', 'book', 'in_bookmarks', )


class BookHighlightForUserSerializer(BookHighlightSerializer):
    class Meta(BookHighlightSerializer.Meta):
        fields = ('id', 'book', 'in_bookmarks', )


# User serialaziers
# =================================================================================
class UserSerializer(serializers.ModelSerializer):
    highlights = BookHighlightForUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'highlights', )
