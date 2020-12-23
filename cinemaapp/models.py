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


class Vip_level(models.Model):
    vlevel = models.CharField(max_length=30, primary_key=True)
    vsale = models.FloatField()


class Vip(models.Model):
    vno = models.AutoField(primary_key=True)
    vname = models.CharField(max_length=30)
    vlevel = models.ForeignKey(Vip_level, on_delete=models.PROTECT)
    vaccount = models.IntegerField()
    vstarttime = models.DateTimeField()


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


class Hall_type(models.Model):
    htype = models.CharField(max_length=30, primary_key=True)
    hvolume = models.IntegerField()


class Hall(models.Model):
    hno = models.AutoField(primary_key=True)
    cno = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    hname = models.CharField(max_length=30)
    htype = models.ForeignKey(Hall_type, on_delete=models.PROTECT)


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


class Ticket(models.Model):
    tno = models.AutoField(primary_key=True)
    sno = models.ForeignKey(Scene, on_delete=models.PROTECT)
    loc = models.IntegerField()
    vno = models.ForeignKey(Vip, on_delete=models.PROTECT)
    price = models.IntegerField()


class All_ticket(models.Model):
    vno = models.IntegerField()
    loc = models.IntegerField()
    cname = models.CharField(max_length=30)
    cloc = models.CharField(max_length=30)
    hname = models.CharField(max_length=30)
    mname = models.CharField(max_length=30)
    ontime = models.DateTimeField()
    offtime = models.DateTimeField()
    price = models.IntegerField()


class Sou(models.Model):
    sono = models.AutoField(primary_key=True)
    mno = models.ForeignKey(Movie, on_delete=models.PROTECT)
    soname = models.CharField(max_length=30)
    soprice = models.IntegerField()
    sostore = models.IntegerField()


class Sousingle(models.Model):
    sosno = models.AutoField(primary_key=True)
    sono = models.ForeignKey(Sou, on_delete=models.PROTECT)
    vno = models.ForeignKey(Vip, on_delete=models.CASCADE)
    price = models.IntegerField()


class Bill(models.Model):
    bno = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30)
    num = models.IntegerField()
    value = models.IntegerField()
    reason = models.CharField(max_length=30)
    date = models.DateTimeField()


class All_sou(models.Model):
    mno = models.IntegerField()
    mname = models.CharField(max_length=30)
    soname = models.CharField(max_length=30)
    soprice = models.IntegerField()
    sostore = models.IntegerField()
    online = models.DateTimeField()
    offline = models.DateTimeField()


class All_sousingle(models.Model):
    mname = models.CharField(max_length=30)
    soname = models.CharField(max_length=30)
    price = models.IntegerField()
    vname = models.CharField(max_length=30)
    vno = models.IntegerField()


class All_Bill(models.Model):
    inbill = models.IntegerField()
    outbill = models.IntegerField()
    date = models.DateField()