from django.contrib import admin
from News.models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'name')

admin.site.register(News,NewsAdmin)