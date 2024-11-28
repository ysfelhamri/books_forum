from django.db import models
from books.models import Book
# Create your models here.
AUTHOR_ROLES = (
    (0,'Story'),
    (1,'Art')
)
class Author(models.Model):
    first_name = models.CharField(max_length=300, blank=True)
    last_name = models.CharField(max_length=300, blank=True)
    alias = models.CharField(max_length=300, blank=True)
    birthday = models.DateField(blank=True,null=True)
    more_info = models.TextField(blank=True)
    image = models.ImageField(upload_to='authors/',blank=True,default='default.jpg')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    books = models.ManyToManyField(Book, through='Author_Book')
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Author_Book(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    author_role = models.IntegerField(choices=AUTHOR_ROLES)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    def __str__(self):
        return self.author.first_name + ' ' + self.author.last_name + ' - ' + self.book.title