from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
from GuildPage.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^hello/$', hello),
                       url(r'^index/$', index),
                       url(r'^policies/$', policies),
                       url(r'^awards/$', awards),
                       url(r'^calendar/$', calendar),
                       url(r'^contact/$', contact),
                       url(r'^forum/$', forum),
                       url(r'^gallery/$', gallery),
                       url(r'^login/$', login),
                       url(r'^members/$', members),
                       url(r'^recruitment/$', recruitment),
                       url(r'^roster/$', roster),
                       url(r'^talents/$', talents),
                       url(r'^video/$', video),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       url(r'^admin/', include(admin.site.urls)),
)
