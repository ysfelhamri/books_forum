from django.contrib import admin
from .models import Book, Genre, Picture, Relationship, Book_Stats
from authors.models import Author_Book
from characters.models import Character_Book
from django.utils.safestring import mark_safe

class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PictureInline(admin.TabularInline):
    model = Picture
    fields = ['picture', 'image_tag', 'title']
    readonly_fields = ['image_tag']
    extra = 1

    def image_tag(self, obj):
        if obj.link:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(obj.link.url))
        return "No Image"
    image_tag.short_description = 'Image'

class AuthorInline(admin.TabularInline):
    model = Author_Book
    extra = 1
    autocomplete_fields = ['author']

class CharacterInline(admin.TabularInline):
    model = Character_Book
    extra = 1
    autocomplete_fields = ['character']

class RelationshipInline(admin.TabularInline):
    model = Relationship
    extra = 1
    fk_name = 'book_original'
    autocomplete_fields = ['book_related']

class Book_StatsInline(admin.TabularInline):
    model = Book_Stats
    fields = ['num_ratings', 'average_score', 'score_rank', 'popularity_rank', 'score_distribution', 'user_statuses']
    readonly_fields = ['num_ratings',  'average_score', 'score_rank', 'popularity_rank', 'score_distribution', 'user_statuses']
    can_delete = False
    max_num = 1

class BookAdmin(admin.ModelAdmin):
    inlines = [Book_StatsInline, PictureInline, RelationshipInline, AuthorInline, CharacterInline]
    autocomplete_fields = ['genres'] 
    search_fields = ['book_related']
    list_filter = ['genres','created_date']
    list_display = ['title','created_date']

admin.site.register(Book,BookAdmin)
admin.site.register(Genre,GenreAdmin)