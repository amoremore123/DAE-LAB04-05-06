from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    biography = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'autor'
        verbose_name_plural = 'autores'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=350)
    body = models.TextField()
    featured_image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
    )
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='articles',
    )
    categories = models.ManyToManyField(Category, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', 'title']
        verbose_name = 'noticia'
        verbose_name_plural = 'noticias'

    def __str__(self):
        return self.title
