from django.contrib import admin
from Policies.models import Policies
from django_summernote.admin import SummernoteModelAdmin


class PoliciesAdmin(SummernoteModelAdmin):
    list_display = ('title', 'body')

admin.site.register(Policies,PoliciesAdmin)