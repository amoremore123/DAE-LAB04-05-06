from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render

from .models import Book


def book_list(request):
	books = Book.objects.select_related('autor').prefetch_related('categories')
	return render(request, 'library/book_list.html', {'books': books})


def book_detail(request, pk):
	book = get_object_or_404(
		Book.objects.select_related('autor', 'autor__profile').prefetch_related(
			'categories', 'publishers', 'publication_set'
		),
		pk=pk,
	)
	return render(request, 'library/book_detail.html', {'book': book})


def book_recommendations(request, pk):
	book = get_object_or_404(Book.objects.prefetch_related('categories'), pk=pk)
	category_ids = book.categories.values_list('pk', flat=True)
	recommendations = (
		Book.objects.filter(categories__in=category_ids)
		.exclude(pk=book.pk)
		.annotate(
			average_score=Avg('ratings__score'),
			rating_count=Count('ratings', distinct=True),
		)
		.filter(average_score__isnull=False)
		.order_by('-average_score', '-rating_count', 'title')
		.distinct()
	)
	return render(
		request,
		'library/book_recommendations.html',
		{'book': book, 'recommendations': recommendations},
	)
from django.shortcuts import render

# Create your views here.
