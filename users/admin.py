from django.contrib import admin
from .models import User, Discussion, Reply, Review, Recommendation, Rating
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm
# Register your models here.

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1
class DiscussionAdmin(admin.ModelAdmin):
    inlines = [ReplyInline]
class CustomUserAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['username', 'email']
    search_fields = ['id', 'username', 'email']
    readonly_fields = ['last_login','date_joined']
    add_form = UserCreationForm
admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Review)
admin.site.register(Recommendation)
admin.site.register(Rating)