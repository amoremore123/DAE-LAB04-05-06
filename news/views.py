from django.shortcuts import get_object_or_404, render

from .models import Article, Category


def home(request):
    articles = Article.objects.select_related('author').prefetch_related('categories')
    return render(request, 'news/home.html', {'articles': articles})


def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related('author').prefetch_related('categories'),
        slug=slug,
    )
    return render(request, 'news/article_detail.html', {'article': article})


def category_articles(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.select_related('author').prefetch_related('categories')
    return render(
        request,
        'news/category_articles.html',
        {'category': category, 'articles': articles},
    )
