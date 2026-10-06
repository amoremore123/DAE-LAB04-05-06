from django.contrib import admin

from .models import Article, Author, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'biography')
    readonly_fields = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'category_list')
    list_filter = ('categories', 'published_at', 'author')
    search_fields = ('title', 'summary', 'body', 'author__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('categories',)
    date_hierarchy = 'published_at'
    list_select_related = ('author',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories')

    @admin.display(description='Categorías')
    def category_list(self, article):
        return ', '.join(category.name for category in article.categories.all())
