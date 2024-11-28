from django.shortcuts import render
from django.views.generic import DetailView
from .models import Character, Character_Book
# Create your views here.
# Need to make a view to show for a specific character

class CharacterDetailView(DetailView):
    model = Character
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        character = self.get_object()
        character_books = Character_Book.objects.filter(character=character)
        context['character_books'] = character_books
        context['title'] = character.name
        return context

