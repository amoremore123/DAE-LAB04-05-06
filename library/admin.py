from django.contrib import admin

from .models import (
	Author,
	AuthorProfile,
	Book,
	BookRating,
	Category,
	Publication,
	Publisher,
)


class AuthorProfileInline(admin.StackedInline):
	model = AuthorProfile
	max_num = 1
	extra = 0


class PublicationInline(admin.TabularInline):
	model = Publication
	extra = 1


class BookRatingInline(admin.TabularInline):
	model = BookRating
	extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'birth_date')
	search_fields = ('name', 'email')
	inlines = (AuthorProfileInline,)


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
	list_display = ('author', 'website')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'autor', 'isbn', 'published_date', 'created_at')
	list_filter = ('categories', 'published_date', 'autor')
	search_fields = ('title', 'isbn', 'autor__name')
	readonly_fields = ('created_at', 'updated_at')
	date_hierarchy = 'published_date'
	list_select_related = ('autor',)
	inlines = (PublicationInline, BookRatingInline)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'website')
	search_fields = ('name',)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
	list_display = ('book', 'publisher', 'publication_date', 'edition')
	list_filter = ('publisher', 'publication_date', 'edition')
	search_fields = ('book__title', 'publisher__name')
	list_select_related = ('book', 'publisher')


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
	list_display = ('book', 'score', 'created_at', 'updated_at')
	list_filter = ('score', 'created_at')
	search_fields = ('book__title', 'book__autor__name', 'comment')
	readonly_fields = ('created_at', 'updated_at')
	list_select_related = ('book', 'book__autor')
