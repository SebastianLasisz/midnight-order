from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    position = models.IntegerField(_("Position"), default=0)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.name


class Forum(models.Model):
    category = models.ForeignKey(Category, related_name='forums')
    name = models.CharField(_("Name"), max_length=255)
    position = models.IntegerField(_("Position"), default=0)
    description = models.TextField(_("Description"), blank=True)
    is_closed = models.BooleanField(_("Is closed"), default=False)

    class Meta:
        ordering = ['position']

    def get_latest_topic(self):
        topics = self.topics.order_by('-last_post__created')
        if topics.count() > 0:
            return topics.all()[0]
        return None

    def get_latest_poster(self):
        latest_topic = self.get_latest_topic()
        if latest_topic:
            return latest_topic.last_post.user
        return '-'

    def count_topics(self):
        return self.topics.count()

    def count_posts(self):
        count = 0
        for topic in self.topics.all():
            count += topic.count_posts()
        return count

    def __unicode__(self):
        return self.name


class Topic(models.Model):
    forum = models.ForeignKey(Forum, related_name='topics')
    name = models.CharField(_("Name"), max_length=255)
    last_post = models.ForeignKey('Post', verbose_name=_("Last post"), related_name='forum_last_post', blank=True, null=True)
    counter = models.IntegerField(_("Counter"), default=0)
    is_closed = models.BooleanField(_("Is closed"), default=False)
    pinned = models.BooleanField(_("Pinned"), default=False)

    class Meta:
        ordering = ['-pinned', '-last_post__created']

    def count_posts(self):
        return self.posts.count()

    def posts_range(self):
        return range(1, 1 + (self.posts.count() - ((self.posts.count()-1) % 20) + 20) / 20)

    def __unicode__(self):
        return self.name

from Register.models import UserProfile


class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts')
    user = models.ForeignKey(UserProfile, related_name='forum_posts')
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    body = models.TextField(_("Body"))
    rating = models.IntegerField(_("Rating"), default=0)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.body


class View(models.Model):
    topic = models.ForeignKey(Topic)
    user = models.ForeignKey(User)
    visited = models.BooleanField(_("Was viewed?"), default=False)

    def __unicode__(self):
        return self.topic.name


class PostRating(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    rating = models.IntegerField(_("Rating"), default=0)
    rated = models.BooleanField(_("Was rated?"), default=False)


class CategoryView(models.Model):
    forum = models.ForeignKey(Forum)
    view = models.ForeignKey(View)