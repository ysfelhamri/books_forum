from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Relationship, Picture, Genre, Book_Stats
from authors.models import Author_Book, Author
from characters.models import Character_Book, Character
from users.models import Review, Recommendation, Discussion, Rating
from django.db.models import Count
from django.core.paginator import Paginator
from users.forms import RatingForm, ReplyForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Sum
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.db.models import F
import json
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

def index(request):
    books = Book.objects.annotate(
        popularity_rank=F('book_stats__popularity_rank')
    ).order_by('popularity_rank')
    paginator = Paginator(books, 18) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/index.html', {'books': page_obj})

def top_books(request):
    books = Book.objects.annotate(
        score_rank=F('book_stats__score_rank')
    ).order_by('score_rank')
    paginator = Paginator(books, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Top Books'

    # Load score, score rank, and authors for each book
    for book in page_obj:
        book_stats = Book_Stats.objects.filter(book=book).first()
        book.score = book_stats.average_score
        book.score_rank = book_stats.score_rank
        book.users = book_stats.num_ratings
        book.popularity_rank = book_stats.popularity_rank
    

    return render(request, 'books/top_books.html', {'books': page_obj, 'title': title})

class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        author_books = Author_Book.objects.filter(book=book)
        character_books = Character_Book.objects.filter(book=book)[:8]
        relationships = Relationship.objects.filter(book_original=book)
        reviews = Review.objects.filter(book=book)[:3]
        recommendations = Recommendation.objects.filter(book_original=book).order_by('-created_date')[:3]
        discussions = Discussion.objects.filter(book=book).order_by('-created_date').annotate(reply_count=Count('discussion_reply'))[:3]
        book_stats = Book_Stats.objects.filter(book=book).first()
        title = book.title
        ch_count = character_books.count() / 2
        if character_books.count() % 2:
            ch_count += 1
        

        # Initialize the form
        if self.request.user.is_authenticated:
            existing_rating = Rating.objects.filter(book=book, user=self.request.user).first()
            form = RatingForm(instance=existing_rating)
        else:
            form = RatingForm()

        context.update({
            'book': book,
            'author_books': author_books,
            'character_books': character_books,
            'relationships': relationships,
            'reviews': reviews,
            'recommendations': recommendations,
            'discussions': discussions,
            'title': title,
            'ch_count': ch_count,
            'form': form,
            'book_stats': book_stats,
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        book = self.object
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to rate a book.')
            return redirect('book-detail', pk=self.object.pk)
    
        form = RatingForm(request.POST)
        if form.is_valid():
            existing_rating = Rating.objects.filter(book=self.object, user=request.user).first()
            if existing_rating:
                rating = form.save(commit=False)
                rating.book = self.object
                rating.user = request.user
    
                if rating.volumes < 0:
                    messages.error(request, 'The volume count cannot be negative.')
                    return self.get(request, *args, **kwargs)
                if rating.chapters < 0:
                    messages.error(request, 'The chapter count cannot be negative.')
                    return self.get(request, *args, **kwargs)
                if rating.volumes > book.volumes:
                    messages.error(request, 'The volume count exceeds the total volumes of the book.')
                    return self.get(request, *args, **kwargs)
                if rating.chapters > book.chapters:
                    messages.error(request, 'The chapter count exceeds the total chapters of the book.')
                    return self.get(request, *args, **kwargs)
    
                existing_rating.volumes = rating.volumes
                existing_rating.chapters = rating.chapters
                existing_rating.score = rating.score
                existing_rating.status = rating.status
                existing_rating.save()
                messages.success(request, 'Your rating has been updated.')
            else:
                # Create new rating
                rating = form.save(commit=False)
                rating.book = self.object
                rating.user = request.user
    
                # Validate volumes and chapters
                if rating.volumes < 0:
                    messages.error(request, 'The volume count cannot be negative.')
                    return self.get(request, *args, **kwargs)
                if rating.chapters < 0:
                    messages.error(request, 'The chapter count cannot be negative.')
                    return self.get(request, *args, **kwargs)
                if rating.volumes > book.volumes:
                    messages.error(request, 'The volume count exceeds the total volumes of the book.')
                    return self.get(request, *args, **kwargs)
                if rating.chapters > book.chapters:
                    messages.error(request, 'The chapter count exceeds the total chapters of the book.')
                    return self.get(request, *args, **kwargs)
    
                rating.save()
                messages.success(request, 'Your rating has been added.')
            return redirect('book-detail', pk=self.object.pk)
        else:
            error_message = form.errors.as_text()
            messages.error(request, 'There was an error with your rating.')
            return self.get(request, *args, **kwargs)


class BookCharactersView(DetailView):
    model = Book
    template_name = 'books/book_characters.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        character_books = Character_Book.objects.filter(book=book)
        author_books = Author_Book.objects.filter(book=book)

        title = book.title

        paginator = Paginator(character_books, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_obj.count = character_books.count()
        context = {
            'book': book,
            'character_books': page_obj,
            'author_books': author_books,
            'title': title,
        }
        return context
    
class BookReviewsView(DetailView):
    model = Book
    template_name = 'books/book_reviews.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews = Review.objects.filter(book=book).order_by('-created_date')
        author_books = Author_Book.objects.filter(book=book)
        title = book.title

        paginator = Paginator(reviews, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_obj.count = reviews.count()
        context = {
            'book': book,
            'reviews': page_obj,
            'author_books': author_books,
            'title': title,
        }
        return context
    
class BookRecommendationsView(DetailView):
    model = Book
    template_name = 'books/book_recommendations.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        recommendations = Recommendation.objects.filter(book_original=book).order_by('-created_date')
        author_books = Author_Book.objects.filter(book=book)
        title = book.title

        paginator = Paginator(recommendations, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_obj.count = recommendations.count()
        context = {
            'book': book,
            'recommendations': page_obj,
            'author_books': author_books,
            'title': title,
        }
        return context
    
class BookPicturesView(DetailView):
    model = Book
    template_name = 'books/book_pictures.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        pictures = Picture.objects.filter(book=book)
        author_books = Author_Book.objects.filter(book=book)
        title = book.title

        paginator = Paginator(pictures, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'book': book,
            'pictures': page_obj,
            'author_books': author_books,
            'title': title,
        }
        return context
    
class BookDiscussionsView(DetailView):
    model = Book
    template_name = 'books/book_discussions.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        discussions = Discussion.objects.filter(book=book).order_by('-created_date').annotate(reply_count=Count('discussion_reply'))
        author_books = Author_Book.objects.filter(book=book)
        title = book.title

        paginator = Paginator(discussions, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        page_obj.count = discussions.count()
        context = {
            'book': book,
            'discussions': page_obj,
            'author_books': author_books,
            'title': title,
        }
        return context
    
class GenreBooksView(ListView):
    model = Book
    template_name = 'books/genre_books.html'
    context_object_name = 'books'
    paginate_by = 18

    def get_queryset(self):
        self.genre = get_object_or_404(Genre, pk=self.kwargs['pk'])
        return Book.objects.filter(genres=self.genre)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = self.genre
        context['title'] = self.genre.name
        return context
    

class BookStatsView(DetailView):
    model = Book
    template_name = 'books/book_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        author_books = Author_Book.objects.filter(book=book)
        book_stats = Book_Stats.objects.filter(book=book).first()
        title = book.title

        if book_stats:
            score_distribution = json.dumps(book_stats.score_distribution)
            user_statuses = json.dumps(book_stats.user_statuses)
        else:
            score_distribution = json.dumps({})
            user_statuses = json.dumps({})

        context.update({
            'book': book,
            'author_books': author_books,
            'book_stats': book_stats,
            'title': title,
            'score_distribution': mark_safe(score_distribution),
            'user_statuses': mark_safe(user_statuses),
        })
        return context
    
def search_view(request):
    query = request.GET.get('query', '')

    books_results = Book.objects.filter(
        Q(title__icontains=query)
    ).values('id', 'title')

    characters_results = Character.objects.filter(
        Q(name__icontains=query)
    ).values('id', 'name')

    authors_results = Author.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    ).values('id', 'first_name', 'last_name')

    authors_results = [
        {'id': author['id'], 'name': f"{author['first_name']} {author['last_name']}"}
        for author in authors_results
    ]

    results = {
        'books': list(books_results),
        'characters': list(characters_results),
        'authors': list(authors_results),
    }

    return JsonResponse(results)