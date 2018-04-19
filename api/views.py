from django.contrib.auth.models import User
from rest_framework import viewsets

from catalogue.models import Book
from catalogue.models import Author
from catalogue.models import Publisher
from catalogue.models import Category
from catalogue.models import BookHighlight

from .serializers.book import BookSerializer
from .serializers.author import AuthorSerializer
from .serializers.publisher import PublisherSerializer
from .serializers.category import CategorySerializer
from .serializers.user import UserSerializer
from .serializers.bookhighlight import BookHighlightSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookHighlightViewSet(viewsets.ModelViewSet):
    queryset = BookHighlight.objects.all()
    serializer_class = BookHighlightSerializer
