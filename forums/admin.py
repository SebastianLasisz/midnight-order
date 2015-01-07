from django.contrib import admin

from forums.models import Category, Forum, Topic, Post, View, CategoryView


class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'position', 'is_closed')


class ViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'visited')


admin.site.register(Category)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(View, ViewAdmin)
admin.site.register(CategoryView)
