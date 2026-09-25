from datetime import date

from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, Category, Publication, Publisher


class LibraryRelationsTests(TestCase):
	def setUp(self):
		self.author = Author.objects.create(name='Autor Test', email='test@example.com')
		self.category = Category.objects.create(name='Test')
		self.publisher = Publisher.objects.create(name='Editorial Test')
		self.book = Book.objects.create(
			title='Libro Test',
			isbn='1234567890123',
			published_date=date(2026, 1, 1),
			autor=self.author,
		)
		self.book.categories.add(self.category)
		Publication.objects.create(
			book=self.book,
			publisher=self.publisher,
			publication_date=date(2026, 1, 1),
			edition=1,
		)

	def test_relations_work_in_both_directions(self):
		self.assertEqual(self.book.autor, self.author)
		self.assertEqual(list(self.author.libros.all()), [self.book])
		self.assertEqual(list(self.book.categories.all()), [self.category])
		self.assertEqual(self.book.publication_set.first().publisher, self.publisher)

	def test_protect_prevents_author_deletion(self):
		with self.assertRaises(ProtectedError):
			self.author.delete()

	def test_detail_view_exposes_related_data(self):
		response = self.client.get(reverse('book-detail', args=[self.book.pk]))
		self.assertContains(response, 'Autor Test')
		self.assertContains(response, 'Test')
		self.assertContains(response, 'Editorial Test')
