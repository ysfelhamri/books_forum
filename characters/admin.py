from django.contrib import admin
from .models import Character

# Register your models here.
class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['name', 'alias', 'description'] 
    
admin.site.register(Character,CharacterAdmin)