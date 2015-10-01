from django.db import models


class Expansion(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Raid(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    expansion = models.ForeignKey(Expansion)

    def __unicode__(self):
        return self.name


class Stage(models.Model):
    id = models.IntegerField(primary_key=True)
    progress = models.CharField(max_length=30)

    def __unicode__(self):
        return self.progress


class Boss(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    raid = models.ForeignKey(Raid)
    progress = models.ForeignKey(Stage)



