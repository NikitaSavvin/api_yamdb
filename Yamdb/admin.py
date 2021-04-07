from django.contrib import admin

from .models import Comment, Review
from users.models import CustomUser


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'score', 'title',)
    search_fields = ('text', 'title')
    list_filter = ('pub_date', 'score',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'created', 'author', 'review',)
    search_fields = ('text',)
    list_filter = ('created', 'author',)
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
