from django.urls import path

from .views import book_detail, book_list, book_recommendations

urlpatterns = [
    path('', book_list, name='book-list'),
    path('libros/<int:pk>/', book_detail, name='book-detail'),
    path(
        'libros/<int:pk>/recomendaciones/',
        book_recommendations,
        name='book-recommendations',
    ),
]