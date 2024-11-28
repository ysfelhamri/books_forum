from django.contrib import admin
from .models import Author
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'alias'] 
admin.site.register(Author,AuthorAdmin)