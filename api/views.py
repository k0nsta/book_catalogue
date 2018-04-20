from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from catalogue.models import Book
from catalogue.models import Author
from catalogue.models import Publisher
from catalogue.models import Category
from catalogue.models import BookHighlight

from .serializers import BookSerializer
from .serializers import AuthorSerializer
from .serializers import PublisherSerializer
from .serializers import CategorySerializer
from .serializers import UserSerializer
from .serializers import BookHighlightSerializer


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
