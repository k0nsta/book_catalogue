# from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('books', views.BooksViewSet)
router.register('authors', views.AuthorsViewSet)
router.register('publishers', views.PublisherViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = router.urls


# urlpatterns = [
#     path('books/', views.BookList.as_view()),
#     path('books/<int:pk>/', views.BookDetail.as_view()),
#     path('authors', views.AuthorList.as_view()),
#     path('authors/<int:pk>/', views.AuthorDetail.as_view()),
# ]
