from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from django_filters import rest_framework as filters

from catalogue import models
from . import serializers as custom_serializers
from . import permissions as custom_permissions
from . import filters as custom_filters


class BooksViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = custom_serializers.BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = custom_filters.BookTitleFilter


class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = custom_serializers.AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = models.Publisher.objects.all()
    serializer_class = custom_serializers.PublisherSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = custom_serializers.CategorySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (custom_permissions.UserReadOnlyOrIsAdmin, )
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(username=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return custom_serializers.UserAdminSerializer
        else:
            return custom_serializers.UserRestrictedSerializer


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = models.Bookmark.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (SessionAuthentication,)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return custom_serializers.BookmarkSerializer
        else:
            return custom_serializers.BookmarkUserSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_staff:
            return queryset.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(user=self.request.user)
