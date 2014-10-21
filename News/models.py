from django.db import models


class News(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=2000)
    name = models.CharField(max_length=20)
    time = models.CharField(max_length=200)
    img = models.CharField(max_length=200, null=True, blank=True)