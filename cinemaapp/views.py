# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

from cinemaapp import models


@require_http_methods(["GET", "POST"])
@csrf_exempt
def show_movie(request):
    print("method: show_movie")
    response = {}
    dict = json.loads(request.body)
    try:
        if dict['curFilm']:
            movies = models.Movie.objects.filter(online__lt=dict['curDate'], offline__gt=dict['curDate'])
        else:
            movies = models.Movie.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", movies))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def login(request):
    print("method: login ")
    response = {}
    dict = json.loads(request.body)
    print("login user_name: " + dict['name'])
    try:
        user = models.User.objects.filter(name=dict['name'], upass=dict['pass'])
        user_dict = json.loads(serializers.serialize("json", user))

        if len(user_dict) == 0:
            response['msg'] = "用户名或密码错误！"
            response['error_num'] = 2
            return JsonResponse(response)

        field_dict = user_dict[0]['fields']
        response['msg'] = 'success'
        response['error_num'] = 0
        if field_dict['type'].strip() == 'vip'.strip():
            response['type'] = 'vip'
            # todo: search vip list
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)