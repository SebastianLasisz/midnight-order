from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=2000)
    name = models.ForeignKey(User)
    time = models.CharField(max_length=200)