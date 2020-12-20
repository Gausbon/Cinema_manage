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


class User(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    upass = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    num = models.IntegerField()


class Vip(models.Model):
    vno = models.AutoField(primary_key=True)
    vname = models.CharField(max_length=30)
    vlevel = models.CharField(max_length=30)
    vaccount = models.IntegerField()
    vstarttime = models.DateTimeField()
    vendtime = models.DateTimeField()


class Employee(models.Model):
    eno = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=30)
    esex = models.CharField(max_length=30)
    ewage = models.IntegerField()
    epart = models.CharField(max_length=30)


class Cinema(models.Model):
    cno = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=30)
    cloc = models.CharField(max_length=30)
    csize = models.CharField(max_length=30)


class Hall(models.Model):
    hno = models.AutoField(primary_key=True)
    cno = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    hname = models.CharField(max_length=30)
    htype = models.CharField(max_length=30)


class Scene(models.Model):
    sno = models.AutoField(primary_key=True)
    cno = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    hno = models.ForeignKey(Hall, on_delete=models.CASCADE)
    mno = models.ForeignKey(Movie, on_delete=models.PROTECT)
    ontime = models.DateTimeField()
    offtime = models.DateTimeField()
    price = models.IntegerField()


class All_scene(models.Model):
    cno = models.IntegerField()
    hno = models.IntegerField()
    hname = models.CharField(max_length=30)
    htype = models.CharField(max_length=30)
    mno = models.IntegerField()
    mname = models.CharField(max_length=30)
    ontime = models.DateTimeField()
    time = models.IntegerField()
    price = models.IntegerField()