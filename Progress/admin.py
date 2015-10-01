from django.contrib import admin

from Progress.models import Raid, Boss, Stage, Expansion


class RaidAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class StageAdmin(admin.ModelAdmin):
    list_display = ('progress', 'id')


class BossAdmin(admin.ModelAdmin):
    list_display = ('name', 'progress', 'raid')


class ExpansionAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


admin.site.register(Raid, RaidAdmin)
admin.site.register(Boss, BossAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Expansion, ExpansionAdmin)