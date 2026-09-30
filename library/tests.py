from datetime import date
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, BookRating, Category, Publication, Publisher


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


class EditorSetupCommandTests(TestCase):
	@patch(
		'library.management.commands.setup_editors.getpass',
		side_effect=['Q7!mV2#zK9$pR4&x', 'Q7!mV2#zK9$pR4&x'],
	)
	def test_editor_can_change_but_not_delete_books(self, mocked_getpass):
		call_command(
			'setup_editors',
			username='test_editor',
			email='editor@example.com',
			stdout=StringIO(),
		)

		user = get_user_model().objects.get(username='test_editor')
		self.assertTrue(user.is_staff)
		self.assertFalse(user.is_superuser)
		self.assertTrue(user.has_perm('library.view_book'))
		self.assertTrue(user.has_perm('library.add_book'))
		self.assertTrue(user.has_perm('library.change_book'))
		self.assertFalse(user.has_perm('library.delete_book'))


class BookRecommendationsTests(TestCase):
	def setUp(self):
		self.author = Author.objects.create(name='Autor Recomendado', email='recommend@example.com')
		self.shared_category = Category.objects.create(name='Ficción')
		self.other_category = Category.objects.create(name='Poesía')
		self.book = Book.objects.create(
			title='Libro de partida',
			isbn='1111111111111',
			published_date=date(2020, 1, 1),
			autor=self.author,
		)
		self.book.categories.add(self.shared_category)
		self.best_match = Book.objects.create(
			title='Mejor coincidencia',
			isbn='2222222222222',
			published_date=date(2021, 1, 1),
			autor=self.author,
		)
		self.best_match.categories.add(self.shared_category)
		BookRating.objects.create(book=self.best_match, score=5)
		BookRating.objects.create(book=self.best_match, score=4)
		self.lower_match = Book.objects.create(
			title='Otra coincidencia',
			isbn='3333333333333',
			published_date=date(2022, 1, 1),
			autor=self.author,
		)
		self.lower_match.categories.add(self.shared_category)
		BookRating.objects.create(book=self.lower_match, score=3)
		self.unrelated = Book.objects.create(
			title='Libro sin categoría compartida',
			isbn='4444444444444',
			published_date=date(2023, 1, 1),
			autor=self.author,
		)
		self.unrelated.categories.add(self.other_category)
		BookRating.objects.create(book=self.unrelated, score=5)

	def test_recommendations_share_category_and_are_ordered_by_average(self):
		response = self.client.get(
			reverse('book-recommendations', args=[self.book.pk]),
		)
		recommendations = list(response.context['recommendations'])

		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			[book.pk for book in recommendations],
			[self.best_match.pk, self.lower_match.pk],
		)
		self.assertContains(response, '4.5/5')
		self.assertNotContains(response, self.unrelated.title)
