from django.contrib import admin

from Progress.models import Raid, Boss, Stage


class RaidAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class StageAdmin(admin.ModelAdmin):
    list_display = ('progress', 'id')


class BossAdmin(admin.ModelAdmin):
    list_display = ('name', 'progress', 'raid')


admin.site.register(Raid, RaidAdmin)
admin.site.register(Boss, BossAdmin)
admin.site.register(Stage, StageAdmin)