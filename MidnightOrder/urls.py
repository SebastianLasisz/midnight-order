from django.conf.urls import patterns, include, url
from Register.views import RegisterDetailView
from django.conf import settings
from django.contrib import admin
from GuildPage.views import *
from Feed.feed import LatestEntries
from django.contrib.auth.decorators import login_required

admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^index/$', index),
                       url(r'^policies/$', policies),
                       url(r'^forums/$', include('forums.urls', namespace='forums')),
                       url(r'^members/$', members),
                       url(r'^recruitment/$', recruitment),
                       url(r'^register/$', register),
                       url(r'^log-out/$', log_out),
                       url(r'^rss/$', LatestEntries()),
                       url(r'^privacy-cookies-policy/$', cookies),
                       url(r'^terms-of-service/$', terms),
                       url(r'^contact-us/$', contact),
                       url(r'^register_complete/$', register_complete),
                       url(r'^profile/$', login_required(upload_pic)),
                       url(r'^thanks/$', thanks),
                       (r'^login/$', 'django.contrib.auth.views.login'),
                       url(r'^admin/$', include(admin.site.urls)),
                       url(r'^recruitment/(?P<slug>[-_\w]+)/$', RegisterDetailView.as_view(), name='register-detail'),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
