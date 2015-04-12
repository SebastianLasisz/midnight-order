from django.contrib.auth.models import User
from Register.models import UserProfile
from forums.models import Post, PostRating


def style(request):
    if request.user.is_authenticated():
        picture = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        return {'style': picture.style}
    else:
        return {}


def post_rating_count(request):
    if request.user.is_authenticated():
        user = UserProfile.objects.get(user=request.user)
        posts = Post.objects.filter(user=user)
        rated_posts = PostRating.objects.filter(post__in=posts).count()
        return {'post_rating_count': rated_posts}
    else:
        return {}