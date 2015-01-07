from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from forums.views import CategoryListView, ForumDetailView, TopicDetailView, TopicCreateView, PostCreateView, LockTopicView, PostEditView, PostRemoveView, PaginatedView


urlpatterns = patterns('',
    url(r'^$', CategoryListView.as_view(), name='overview'),
    url(r'^(?P<pk>\d+)/$', ForumDetailView.as_view(), name='forum'),
    url(r'^(?P<forum_id>\d+)/create/$', login_required(TopicCreateView.as_view()), name='topic_create'),
    #url(r'^topic/(?P<pk>\d+)/$', TopicDetailView.as_view(), name='topic'),
    url(r'^topic/(?P<pk>\d+)/page(?P<page>[0-9]+)/$', PaginatedView.as_view(), name='topic'),
    url(r'^post/(?P<pk>\d+)/edit/$', PostEditView.as_view(), name='edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', PostRemoveView.as_view(), name='remove'),
    url(r'^topic/(?P<pk>\d+)/lock/$', LockTopicView.as_view(), name='lock_topic'),
    url(r'^topic/(?P<pk>\d+)/create/$', login_required(PostCreateView.as_view()), name='post_create'),
)
