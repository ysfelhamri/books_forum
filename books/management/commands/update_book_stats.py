from django.core.management.base import BaseCommand
from django.db.models import Avg, Count
from books.models import Book, Book_Stats
from users.models import Rating

class Command(BaseCommand):
    help = 'Update book statistics'

    def handle(self, *args, **kwargs):
        books = Book.objects.all()

        book_stats = []

        for book in books:
            ratings = Rating.objects.filter(book=book)
            num_ratings = ratings.count()
            average_score = ratings.aggregate(Avg('score'))['score__avg'] or 0
            
            score_distribution = ratings.values('score').annotate(count=Count('score')).order_by('score')

            user_statuses = ratings.values('status').annotate(count=Count('status')).order_by('status')

            book_stats.append({
                'book': book,
                'average_score': average_score,
                'num_ratings': num_ratings,
                'score_distribution': list(score_distribution),
                'user_statuses': list(user_statuses),
            })

        sorted_by_score = sorted(book_stats, key=lambda x: x['average_score'], reverse=True)
        for rank, book_stat in enumerate(sorted_by_score, start=1):
            Book_Stats.objects.update_or_create(
                book=book_stat['book'],
                defaults={
                    'average_score': book_stat['average_score'],
                    'score_rank': rank,
                    'num_ratings': book_stat['num_ratings'],
                    'score_distribution': book_stat['score_distribution'],
                    'user_statuses': book_stat['user_statuses'],
                }
            )

        sorted_by_popularity = sorted(book_stats, key=lambda x: x['num_ratings'], reverse=True)
        for rank, book_stat in enumerate(sorted_by_popularity, start=1):
            Book_Stats.objects.update_or_create(
                book=book_stat['book'],
                defaults={
                    'popularity_rank': rank,
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated books statistics'))
