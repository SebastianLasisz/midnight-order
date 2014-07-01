from django.db import models

# Create your models here.


class Register(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField(max_length=4)
    country = models.CharField(max_length=200)
    about_yourself = models.CharField(max_length=500)
    username = models.CharField(max_length=50)
    class_1 = models.CharField(max_length=10)
    spec = models.CharField(max_length=10)
    wol_logs = models.CharField(max_length=30)
    professions = models.CharField(max_length=200)
    previous_guilds = models.CharField(max_length=200)
    contacs = models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    questions = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40)