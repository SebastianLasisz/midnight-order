from django.db import models

# Create your models here.


class Member(models.Model):
    name = models.CharField(max_length=30)
    level = models.IntegerField(max_length=4)
    thumbnail = models.CharField(max_length=200)
    class_number = models.IntegerField(max_length=3)
    class_name = models.CharField(max_length=50)
    spec = models.CharField(max_length=10)
    rank = models.IntegerField(max_length=2)
    rank_name = models.CharField(max_length=15)
    armory = models.CharField(max_length=200)