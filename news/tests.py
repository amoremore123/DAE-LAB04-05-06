from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Author, Category


class NewsPortalTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name='Ana Torres',
            email='ana@example.com',
        )
        self.technology = Category.objects.create(
            name='Tecnología',
            slug='tecnologia',
        )
        self.culture = Category.objects.create(
            name='Cultura',
            slug='cultura',
        )
        self.article = Article.objects.create(
            title='Django simplifica el trabajo editorial',
            slug='django-simplifica-el-trabajo-editorial',
            summary='Una noticia de prueba para la portada del portal.',
            body='El contenido llega desde la base de datos.',
            author=self.author,
            published_at=timezone.make_aware(datetime(2026, 10, 1, 9, 0)),
        )
        self.article.categories.add(self.technology)
        self.other_article = Article.objects.create(
            title='Agenda cultural de octubre',
            slug='agenda-cultural-de-octubre',
            summary='Una noticia que solo pertenece a la categoría cultural.',
            body='Contenido cultural.',
            author=self.author,
            published_at=timezone.make_aware(datetime(2026, 9, 30, 9, 0)),
        )
        self.other_article.categories.add(self.culture)

    def test_home_uses_the_article_card_for_each_article(self):
        response = self.client.get(reverse('news:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/home.html')
        self.assertTemplateUsed(response, 'news/_article_card.html')
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.other_article.title)

    def test_category_page_only_shows_its_articles(self):
        response = self.client.get(
            reverse('news:category', args=[self.technology.slug]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/category_articles.html')
        self.assertContains(response, self.article.title)
        self.assertNotContains(response, self.other_article.title)

    def test_detail_escapes_html_saved_in_the_article_body(self):
        self.article.body = '<strong>Texto de prueba</strong>'
        self.article.save(update_fields=['body'])

        response = self.client.get(
            reverse('news:detail', args=[self.article.slug]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.name)
        self.assertContains(response, self.technology.name)
        self.assertIn(b'&lt;strong&gt;Texto de prueba&lt;/strong&gt;', response.content)
