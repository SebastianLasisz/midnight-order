from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
from django.views.generic import ListView, DetailView, FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from forums.forms import TopicCreateForm, PostCreateForm, PostEditForm
from forums.models import Category, Topic, Forum, Post, View, CategoryView, PostRating
from Register.models import UserProfile


class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        categories = []
        breaking = False
        if self.request.user.is_authenticated():
            for c in self.object_list.all():
                forums = Forum.objects.filter(category=c)
                for f in forums:
                    topics = Topic.objects.filter(forum=f)
                    if topics:
                        for t in topics:
                            view = View.objects.filter(topic=t, user=self.request.user)
                            for v in view:
                                if not v.visited:
                                    cv = CategoryView(forum=f, view=v)
                                    categories.insert(0, cv)
                                    breaking = True
                            if breaking:
                                breaking = False
                                break
        context['view_categories'] = categories
        return context


class ForumDetailView(DetailView):
    model = Forum

    def get_context_data(self, **kwargs):
        context = super(ForumDetailView, self).get_context_data(**kwargs)
        topics = []
        if self.request.user.is_authenticated():
            for t in self.object.topics.all():
                if not View.objects.filter(topic=t, user=self.request.user):
                    view = View(topic=t, user=self.request.user, visited=False)
                    view.save()
                    topics += View.objects.filter(topic=t, user=self.request.user)
                else:
                    topics += View.objects.filter(topic=t, user=self.request.user)
        forum = Forum.objects.filter(id=self.kwargs.get('pk'))
        topics_in_category = Topic.objects.filter(forum=forum)
        first_posts = []
        for tic in topics_in_category:
            first_posts += Post.objects.filter(topic=tic)[:1]
        context['view_topic'] = topics
        context['first_post'] = first_posts
        return context


class TopicDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        try:
            view = View.objects.get(user=self.request.user, topic=self.object)
            view.visited = True
            view.save()
        except:
            if self.request.user.is_authenticated():
                view = View(user=self.request.user, topic=self.object, visited=True)
                view.save()
        self.object.counter += 1
        self.object.save()
        return context

    model = Topic


class PaginatedView(ListView):
    def get_context_data(self, **kwargs):
        context = super(PaginatedView, self).get_context_data(**kwargs)
        topic = Topic.objects.filter(id=self.kwargs.get('pk'))
        context['first_post'] = Post.objects.filter(topic=topic)[0]
        return context

    def get_queryset(self):
        model = Topic.objects.get(id=self.kwargs.get('pk'))
        try:
            view = View.objects.get(user=self.request.user, topic=model)
            view.visited = True
            view.save()
        except:
            if self.request.user.is_authenticated():
                view = View(user=self.request.user, topic=model, visited=True)
                view.save()
        model.counter += 1
        model.save()
        return Post.objects.filter(topic=model)

    template_name = 'forums/topic_detail.html'
    context_object_name = "topic"
    paginate_by = 20


class TopicCreateView(FormView):
    template_name = 'forums/topic_create.html'
    form_class = TopicCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.forum = Forum.objects.get(id=kwargs.get('forum_id', None))
        if self.forum.is_closed and not request.user.is_staff:
            messages.error(request, _("You do not have the permissions to create a topic."))
            return HttpResponseRedirect('/forums/')
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
        users = User.objects.all()
        for u in users:
            view = View(user=u, topic=topic, visited=False)
            view.save()

        self.success_url = ('/forums/topic/' + str(topic.id) + '/page1')

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
            topic_page = self.topic.posts_range()[-1]
            return HttpResponseRedirect('/forums/topic/' + str(self.topic.id) + '/page' + str(topic_page))
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        body = form.cleaned_data['message']
        user = UserProfile.objects.get(user=User.objects.get(username=self.request.user.username))

        post = Post(topic=self.topic, body=body, user=user)
        post.save()
        post.topic.last_post = post
        post.topic.save()

        view = View.objects.filter(topic=self.topic)
        for v in view:
            v.visited = False
            v.save()
        topic_page = self.topic.posts_range()[-1]
        self.success_url = ('/forums/topic/' + str(self.topic.id) + '/page' + str(topic_page))

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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


from django.template import RequestContext


class PostEditView(FormView):
    template_name = 'forums/edit_post.html'
    form = PostEditForm()

    def form_valid(self, form):
        body = form.cleaned_data['message']
        user = UserProfile.objects.get(user=User.objects.get(username=self.request.user.username))
        post = Post(topic=self.topic, body=body, user=user)
        post.save()
        post.topic.last_post = post
        post.topic.save()

        self.success_url = reverse('forums:topic', args=[self.topic.id])

        return super(PostCreateView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk', None)
        self.post = Post.objects.get(id=kwargs.get('pk', None))
        name = self.post.user.user.username
        if request.method == 'POST':
            form = PostEditForm(request.POST)
            if form.is_valid():
                post = Post.objects.get(id=kwargs.get('pk', None))
                post.body = form.cleaned_data['message']
                post.save()
            else:
                return render_to_response('forums/edit_post.html', locals(), RequestContext(request))
            topic_page = self.post.topic.posts_range()[-1]
            return HttpResponseRedirect('/forums/topic/' + str(self.post.topic.id) + '/page' + str(topic_page))
        else:
            form = PostEditForm(initial={'message': self.post})
        return render(request, 'forums/edit_post.html', {'form': form, 'pk': self.pk, 'post': self.post, 'name': name})


class PostRemoveView(FormView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.groups.all()[0].name == "Officer":
            try:
                self.pk = kwargs.get('pk', None)
                self.post = Post.objects.get(id=kwargs.get('pk', None))
                if self.post.topic.last_post != self.post:
                    self.post.delete()
                else:
                    if self.post.topic.count_posts() == 1:
                        self.post.topic.delete()
                        return HttpResponseRedirect('/forums/')
                    else:
                        posts = Post.objects.filter(topic=self.post.topic)
                        posts_reversed = list(reversed(posts))
                        self.post.topic.last_post = posts_reversed[1]
                        self.post.topic.save()
                        self.post.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except EnvironmentError:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        self.pk = kwargs.get('pk', None)
        self.post = Post.objects.get(id=kwargs.get('pk', None))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class PinTopicView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(PinTopicView, self).get_context_data(**kwargs)
        if self.request.user.groups.all()[0].name == "Officer":
            if self.object.pinned:
                self.object.pinned = False
            else:
                self.object.pinned = True
        self.object.save()
        return context

    model = Topic

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        object = Topic.objects.get(id=self.pk)
        if self.request.user.groups.all()[0].name == "Officer":
            if object.pinned:
                object.pinned = False
            else:
                object.pinned = True
        object.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class UpRatePostView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        object = Post.objects.get(id=self.pk)
        user = request.user
        rated_post = PostRating.objects.filter(user=user, post=object)
        try:
            if rated_post[0].rated:
                error = "You can't rate multiple times the same post."
            else:
                object.rating += 1
                object.save()
                rated_post.rated = True
                rated_post.rating = 1
                rated_post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except:
            object.rating += 1
            object.save()
            rated_post = PostRating(user=user, post=object, rating=1, rated=True)
            rated_post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class DownRatePostView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk')
        object = Post.objects.get(id=self.pk)
        user = request.user
        rated_post = PostRating.objects.filter(user=user, post=object)
        try:
            if rated_post[0].rated:
                error = "You can't rate multiple times the same post."
            else:
                object.rating -= 1
                object.save()
                rated_post.rated = True
                rated_post.rating = -1
                rated_post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except:
            object.rating -= 1
            object.save()
            rated_post = PostRating(user=user, post=object, rating=-1, rated=True)
            rated_post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))