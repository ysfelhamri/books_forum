from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book

# Create your models here.
DISCUSSION_TYPES = (
    (0,'Chapter Discussion'),
    (-1,'Other')
)
VERDICTS = (
    (0,'Recommended'),
    (1,'Mixed Feelings'),
    (2,'Not Recommended')
)
SCORES = (
    (1,'1 - Terrible'),
    (2,'2 - Very Bad'),
    (3,'3 - Bad'),
    (4,'4 - Below Average'),
    (5,'5 - Average'),
    (6,'6 - Above Average'),
    (7,'7 - Good'),
    (8,'8 - Very Good'),
    (9,'9 - Excellent'),
    (10,'10 - Masterpiece')
)
STATUS = (
    (0,'Reading'),
    (1,'Completed'),
    (2,'On-Hold'),
    (3,'Dropped'),
    (4,'Plan to Read')
)

class User(AbstractUser):
    pass
    username = models.CharField(max_length=300, unique=True)
    email = models.EmailField(max_length=300, unique=True)
    first_name = models.CharField(max_length=300, blank=True)
    last_name = models.CharField(max_length=300, blank=True)
    birthday = models.DateField(blank=True,null=True)
    image = models.ImageField(upload_to='users/',default='default.jpg')
    about = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    discussions = models.ManyToManyField(Book, through='Discussion', related_name='discussion')
    replies = models.ManyToManyField('Discussion', through='Reply', related_name='reply')
    reviews = models.ManyToManyField(Book, through='Review', related_name='review')
    recommendations = models.ManyToManyField(Book, through='Recommendation',through_fields=('user', 'book_original'), related_name='recommendation')
    ratings = models.ManyToManyField(Book, through='Rating', related_name='rating')


class Discussion(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_discussion')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_discussion')
    title = models.CharField(max_length=300)
    discussion_type = models.IntegerField(choices=DISCUSSION_TYPES)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Discussion"
        verbose_name_plural = "Discussions"
    def __str__(self):
        return self.title

class Reply(models.Model):
    discussion = models.ForeignKey(Discussion,on_delete=models.CASCADE,related_name='discussion_reply')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_reply')
    reply = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"

class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_review')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_review')
    verdict = models.IntegerField(choices=VERDICTS)
    review = models.TextField()
    chapters_read_on_review = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Recommendation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book_original = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_original')
    book_recommended = models.ForeignKey(Book,on_delete=models.CASCADE, related_name='book_recommended')
    recommendation = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Rating(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_rating')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_rating')
    volumes = models.IntegerField(default=0)
    chapters = models.IntegerField(default=0)
    score = models.IntegerField(choices=SCORES)
    status = models.IntegerField(choices=STATUS, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
