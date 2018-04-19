from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('books', views.BooksViewSet)
router.register('authors', views.AuthorsViewSet)
router.register('publishers', views.PublisherViewSet)
router.register('categories', views.CategoryViewSet)
router.register('users', views.UserViewSet)
router.register('highlights', views.BookHighlightViewSet)

urlpatterns = []

urlpatterns += router.urls
