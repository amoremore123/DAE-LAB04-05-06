from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<slug:slug>/', views.category_articles, name='category'),
    path('<slug:slug>/', views.article_detail, name='detail'),
]
