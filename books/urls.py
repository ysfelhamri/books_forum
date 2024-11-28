from django.urls import path

from . import views
from .views import search_view

urlpatterns = [
    path("", views.index, name="index"),
    path("top/", views.top_books, name="top-books"),
    path("books/genre/<int:pk>", views.GenreBooksView.as_view(), name="genre-books"),
    path("book/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("book/<int:pk>/characters/", views.BookCharactersView.as_view(), name="book-characters"),
    path("book/<int:pk>/reviews/", views.BookReviewsView.as_view(), name="book-reviews"),
    path("book/<int:pk>/recommendations/", views.BookRecommendationsView.as_view(), name="book-recommendations"),
    path("book/<int:pk>/pictures/", views.BookPicturesView.as_view(), name="book-pictures"),
    path("book/<int:pk>/discussions/", views.BookDiscussionsView.as_view(), name="book-discussions"),
    path("book/<int:pk>/stats/", views.BookStatsView.as_view(), name="book-stats"),
    path('search/', search_view, name='search'),
]