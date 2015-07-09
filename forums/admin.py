from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from forums.models import Category, Forum, Topic, Post, View, CategoryView, PostRating


class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'position', 'is_closed')


class ViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'visited')


class RateAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'post', 'rated')


class PostAdmin(SummernoteModelAdmin):
    list_display = ('body', 'rating')

admin.site.register(Category)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic)
admin.site.register(Post, PostAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(PostRating, RateAdmin)
