from django.contrib import admin

from .models import Author
from .models import Book
from .models import Category
from .models import Publisher


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author
    exclude = ('is_void', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    exclude = ('is_void', )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    model = Publisher
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

    class Meta:
        model = Book
