# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.


class Movie(models.Model):
    mno = models.AutoField(primary_key=True)
    mname = models.CharField(max_length=30)
    director = models.CharField(max_length=30)
    actor = models.CharField(max_length=30)
    time = models.IntegerField()
    type = models.CharField(max_length=30)
    online = models.DateTimeField()
    offline = models.DateTimeField()