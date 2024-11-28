from django.urls import path
from .views import CharacterDetailView
from . import views

urlpatterns = [
    path('character/<int:pk>/', CharacterDetailView.as_view(), name='character-detail'),
]