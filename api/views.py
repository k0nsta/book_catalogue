from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication


from catalogue.models import Book
from catalogue.models import Author
from catalogue.models import Publisher
from catalogue.models import Category
from catalogue.models import Bookmark

from .serializers import BookSerializer
from .serializers import AuthorSerializer
from .serializers import PublisherSerializer
from .serializers import CategorySerializer
from .serializers import UserSerializer
from .serializers import BookmarkSerializer, BookmarkUserSerializer


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
    permission_classes = (permissions.IsAdminUser, )
    authentication_classes = (SessionAuthentication,)


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (SessionAuthentication,)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return BookmarkSerializer
        else:
            return BookmarkUserSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_superuser:
            return queryset.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            serializer.save(user=self.request.user)
