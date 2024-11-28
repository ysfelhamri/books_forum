from django.db import models

# Create your models here.
BOOK_STATUS = (
    (0,'Completed'),
    (1,'Publishing'),
    (-1,'On Hiatus')
)
RELATIONSHIP_TYPES = (
    (0,'Prequel'),
    (1,'Sequel'),
    (2,'Alternative Version'),
    (3,'Side Story'),
    (4,'Parent Story'),
    (-1,'Other')
)

class Book(models.Model):
    title = models.CharField(max_length=300)
    alternative_titles = models.TextField(blank=True)
    volumes = models.IntegerField(blank=True)
    chapters = models.IntegerField(blank=True)
    status = models.IntegerField(choices=BOOK_STATUS,default=1)
    synopsis = models.TextField(blank=True)
    background = models.TextField(blank=True)
    cover = models.ImageField(upload_to='books/covers/',default='default_book.jpg')
    publishing_start_date = models.DateField(blank=True,null=True)
    publishing_end_date = models.DateField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    relationships = models.ManyToManyField('self', through='Relationship', symmetrical=False)
    genres = models.ManyToManyField('Genre')
    def __str__(self):
        return self.title

class Relationship(models.Model):
    book_original = models.ForeignKey(Book, related_name='Relationship_from_set',on_delete=models.CASCADE)
    book_related = models.ForeignKey(Book,related_name='Relationship_to_set',on_delete=models.CASCADE, verbose_name='Related Book')
    relationship_type = models.IntegerField(choices=RELATIONSHIP_TYPES)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Related Entry"
        verbose_name_plural = "Related Entries"
    def __str__(self):
        return self.book_original.title + ' - ' + self.book_related.title
    def save(self, *args, **kwargs):
            mirror_exists = Relationship.objects.filter(
                book_original=self.book_related,
                book_related=self.book_original,
                relationship_type=self.get_mirror_type()
            ).exists()

            if not mirror_exists:
                super().save(*args, **kwargs) 
                
                Relationship.objects.create(
                    book_original=self.book_related,
                    book_related=self.book_original,
                    relationship_type=self.get_mirror_type()
                )
            else:
                super().save(*args, **kwargs)
    def get_mirror_type(self):
        if self.relationship_type == 0:
            return 1  
        elif self.relationship_type == 1:
            return 0  
        elif self.relationship_type == 3:
            return 4
        elif self.relationship_type == 4:
            return 3
        else:
            return self.relationship_type

class Genre(models.Model):
    name = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return self.name


class Picture(models.Model):
    picture = models.ImageField(upload_to='books/',default='default_book.jpg')
    title = models.CharField(max_length=300,blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Book_Stats(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    num_ratings = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    score_rank = models.IntegerField(default=0)
    popularity_rank = models.IntegerField(default=0)
    score_distribution = models.JSONField(default=dict)
    user_statuses = models.JSONField(default=dict)
    
    def __str__(self):
        return f'Stats for {self.book.title}'