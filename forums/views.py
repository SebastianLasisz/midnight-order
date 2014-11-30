from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from forums.forms import TopicCreateForm, PostCreateForm
from forums.models import Category, Topic, Forum, Post
from Register.models import UserProfile


class CategoryListView(ListView):
    model = Category


class ForumDetailView(DetailView):
    model = Forum


class TopicDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)

        self.object.counter += 1
        self.object.save()
        return context
    model = Topic


class TopicCreateView(FormView):
    template_name = 'forums/topic_create.html'
    form_class = TopicCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.forum = Forum.objects.get(id=kwargs.get('forum_id', None))
        if self.forum.is_closed and not request.user.is_staff:
            messages.error(request, _("You do not have the permissions to create a topic."))
            return HttpResponseRedirect(reverse_lazy('forums:forum', args=[self.forum.id]))
        return super(TopicCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        topic_name = form.cleaned_data['topic']
        post_body = form.cleaned_data['message']
        user = UserProfile.objects.get(user=User.objects.get(username=self.request.user.username))
        topic = Topic(forum=self.forum, name=topic_name, counter=0)
        topic.save()
        post = Post(topic=topic, body=post_body, user=user)
        post.save()
        topic.last_post = post
        topic.save()

        self.success_url = reverse('forums:topic', args=[topic.id])

        return super(TopicCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TopicCreateView, self).get_context_data(**kwargs)
        context['forum'] = Forum.objects.get(id=self.kwargs.get('forum_id', None))
        username = self.request.user.username
        picture = UserProfile.objects.get(user=User.objects.get(username=username))
        context['avatar'] = picture.avatar
        return context


class PostCreateView(FormView):
    template_name = 'forums/post_create.html'
    form_class = PostCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.topic = Topic.objects.get(id=kwargs.get('pk', None))
        if self.topic.forum.is_closed and not request.user.is_staff:
            messages.error(request, _("You do not have the permissions to create a topic."))
            return HttpResponseRedirect(reverse_lazy('forums:forum', args=[self.topic.forum.id]))
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        body = form.cleaned_data['message']
        user = UserProfile.objects.get(user=User.objects.get(username=self.request.user.username))

        post = Post(topic=self.topic, body=body, user=user)
        post.save()
        post.topic.last_post = post
        post.topic.save()

        self.success_url = reverse('forums:topic', args=[self.topic.id])

        return super(PostCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['topic'] = Topic.objects.get(id=self.kwargs.get('pk', None))
        username = self.request.user.username
        picture = UserProfile.objects.get(user=User.objects.get(username=username))
        context['avatar'] = picture.avatar
        return context


class LockTopicView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(LockTopicView, self).get_context_data(**kwargs)
        if self.request.user.groups.all()[0].name == "Officer":
            if self.object.is_closed:
                self.object.is_closed = False
            else:
                self.object.is_closed = True
        self.object.save()
        return context
    model = Topic

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        object = Topic.objects.get(id=self.pk)
        if self.request.user.groups.all()[0].name == "Officer":
            if object.is_closed:
                object.is_closed = False
            else:
                object.is_closed = True
        object.save()
        return HttpResponseRedirect('/forums/topic/'+self.pk)