from django.db import models
from books.models import Book

# Create your models here.
# Need to translate diagram to a model here

CHARACTER_ROLES = (
    (0,'Main'),
    (1,'Supporting')
)
class Character(models.Model):
    name = models.CharField(max_length=300)
    alias = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='characters/',blank=True,default='default.jpg')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    books = models.ManyToManyField(Book, through='Character_Book')
    def __str__(self):
        return self.name

class Character_Book(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    character = models.ForeignKey(Character,on_delete=models.CASCADE)
    character_role = models.IntegerField(choices=CHARACTER_ROLES)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"
    def __str__(self):
        return self.character.name + ' - ' + self.book.title