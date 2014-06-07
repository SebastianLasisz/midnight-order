from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from GuildPage.views import *
from Feed.feed import LatestEntries

admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^index/$', index),
                       url(r'^policies/$', policies),
                       url(r'^calendar/$', calendar),
                       url(r'^contact/$', contact),
                       url(r'^forum/$', forum),
                       url(r'^login/$', login),
                       url(r'^members/$', members),
                       url(r'^recruitment/$', recruitment),
                       url(r'^feed/$', LatestEntries()),
                       url(r'^registered/([\w-]+)/$', index),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'^admin/', include(admin.site.urls)),
)
