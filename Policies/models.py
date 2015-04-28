from django.db import models


class Policies(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=40000)