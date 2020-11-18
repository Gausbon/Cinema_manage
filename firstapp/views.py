# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse
from firstapp import models
from datetime import datetime


def home(request):
    #QuerySet = models.Movie.objects.count()
    str = '目前上映电影: '
    for p in models.Movie.objects.raw('SELECT * FROM [cinema].[dbo].[movie]'):
        str = str + p.mname + ' '
    return HttpResponse(str)