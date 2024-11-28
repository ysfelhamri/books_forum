from django.shortcuts import render
from django.views.generic import DetailView
from .models import Author, Author_Book
# Create your views here.
class AuthorDetailView(DetailView):
    model = Author
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        author_books = Author_Book.objects.filter(author=author)
        context['author_books'] = author_books
        context['title'] = author.first_name + ' ' + author.last_name
        return context