from django.contrib import admin

from .models import Author
from .models import Book
from .models import Category
from .models import Publisher
from .models import BookHighlight


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    exclude = ('is_void', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('is_void', )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    exclude = ('is_void',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'publisher',
        'category',
        'create_date',
        'modified_date',
        'is_active',
    )
    exclude = ('is_void', )


@admin.register(BookHighlight)
class UserToBookRelationsAdmin(admin.ModelAdmin):
    list_display = (
            'user',
            'book',
            'in_bookmarks',
        )

    exclude = ('is_void', )
