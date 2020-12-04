# -*- coding:utf-8 -*-
import select
from django.forms import model_to_dict
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json

from cinemaapp import models

@require_http_methods(["GET"])
def show_movie(request):
    print("method: show_movie")
    response = {}
    try:
        movies = models.Movie.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", movies))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
