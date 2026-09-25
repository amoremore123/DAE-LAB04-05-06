from django.contrib import admin
from .models import Author, AuthorProfile, Book, Category, Publication, Publisher


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'birth_date')
	search_fields = ('name', 'email')


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
	list_display = ('author', 'website')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'autor', 'isbn', 'published_date')
	list_filter = ('categories', 'autor')
	search_fields = ('title', 'isbn')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	search_fields = ('name',)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
	list_display = ('book', 'publisher', 'publication_date', 'edition')
