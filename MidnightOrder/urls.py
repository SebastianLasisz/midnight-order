from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

from Register.views import RegisterDetailView
from GuildPage.views import *
from Feed.feed import LatestEntries


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^index/$', index),
                       url(r'^news/(?P<pk>\d+)/$', paged_index),
                       url(r'^policies/$', policies),
                       url(r'^forums/', include('forums.urls', namespace='forums')),
                       url(r'^members/$', members),
                       url(r'^recruitment/$', recruitment),
                       url(r'^register/$', register),
                       url(r'^add_news/$', login_required(add_news)),
                       url(r'^log-out/$', log_out),
                       url(r'^rss/$', LatestEntries()),
                       url(r'^privacy-cookies-policy/$', cookies),
                       url(r'^terms-of-service/$', terms),
                       url(r'^contact-us/$', contact),
                       url(r'^register_complete/$', register_complete),
                       url(r'^profile/$', login_required(profile)),
                       url(r'^thanks/$', thanks),
                       url(r'^credits/$', credit),
                       url(r'^ajax_test/$', ajax_test),
                       url(r'^forums/new_content/$', login_required(new_content)),
                       url(r'^ajax_upvote/$', ajax_upvote),
                       url(r'^media/$', media),
                       (r'^summernote/', include('django_summernote.urls')),
                       (r'^messages/', include('django_messages.urls')),
                       (r'^login/$', 'django.contrib.auth.views.login'),
                       (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^recruitment/(?P<slug>[-_\w]+)/$', RegisterDetailView.as_view(), name='register-detail'),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                       (r'^media/&', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
