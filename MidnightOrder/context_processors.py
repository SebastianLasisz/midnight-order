from django.contrib.auth.models import User
from Register.models import UserProfile


def style(request):
    if request.user.is_authenticated():
        picture = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
        return {'style': picture.style}
    else:
        return {}
