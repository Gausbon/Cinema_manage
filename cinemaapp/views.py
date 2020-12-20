# -*- coding:utf-8 -*-
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, ProtectedError
import json

from cinemaapp import models


@require_http_methods(["GET", "POST"])
@csrf_exempt
def show_movie(request):
    print("method: show_movie")
    response = {}
    dict = json.loads(request.body)
    try:
        t = dict['t']
        if dict['r']:
            t = '-' + t

        if dict['curFilm']:
            movies = models.Movie.objects.filter(online__lt=dict['curDate'], offline__gt=dict['curDate']).order_by(t)
        else:
            movies = models.Movie.objects.filter().order_by(t)
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
    print("method: login")
    response = {}
    dict = json.loads(request.body)
    print("login user_name: " + dict['name'])
    try:
        user = models.User.objects.filter(name=dict['name'], upass=dict['pass'])
        user_dict = json.loads(serializers.serialize("json", user))

        if len(user_dict) == 0:
            print("login failed: incorrect password or username")
            response['msg'] = "用户名或密码错误！"
            response['error_num'] = 2
            return JsonResponse(response)

        field_dict = user_dict[0]['fields']
        response['msg'] = 'success'
        response['error_num'] = 0
        if field_dict['type'].strip() == 'vip'.strip():
            print("login vip, vip no." + str(field_dict['num']))
            response['type'] = 'vip'
            response['id'] = field_dict['num']
        elif field_dict['type'].strip() == '电影管理'.strip():
            print("login employee, employee no." + str(field_dict['num']))
            response['type'] = 'movie'
            response['id'] = field_dict['num']
        else:
            print("login boss, boss no." + str(field_dict['num']))
            response['type'] = 'boss'
            response['id'] = field_dict['num']

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def show_vip(request):
    print("method: show vip")
    response = {}
    dict = json.loads(request.body)
    print("show vip id: " + dict['id'])
    try:
        vip = models.Vip.objects.filter(vno=int(dict['id']))
        response['msg'] = 'success'
        response['error_num'] = 0
        response['list'] = json.loads(serializers.serialize("json", vip))[0]['fields']
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def show_employee(request):
    print("method: show vip")
    response = {}
    dict = json.loads(request.body)
    print("show employee id: " + dict['id'])
    try:
        employee = models.Employee.objects.filter(~Q(epart='boss'), eno=int(dict['id']))
        response['msg'] = 'success'
        response['error_num'] = 0
        response['list'] = json.loads(serializers.serialize("json", employee))[0]['fields']
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def show_boss(request):
    print("method: show vip")
    response = {}
    dict = json.loads(request.body)
    print("show boss id: " + dict['id'])
    try:
        boss = models.Vip.objects.filter(epart='boss', eno=int(dict['id']))
        response['msg'] = 'success'
        response['error_num'] = 0
        response['list'] = json.loads(serializers.serialize("json", boss))[0]['fields']
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def update_movie(request):
    print("method: update movie")
    response = {}
    dict = json.loads(request.body)
    print("update movie id: " + dict['last_name'])
    try:
        m = models.Movie.objects.get(mname=dict['last_name'])
        m.mname = dict['mname']
        m.director = dict['director']
        m.actor = dict['actor']
        m.time = dict['time']
        m.type = dict['type']
        m.online = dict['online']
        m.offline = dict['offline']
        m.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        if type(e) == IntegrityError:
            response['error_num'] = 2
        else:
            response['error_num'] = 1
        response['msg'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def insert_movie(request):
    print("method: insert movie")
    response = {}
    dict = json.loads(request.body)
    print(dict)
    print("insert movie")
    try:
        models.Movie.objects.create(
            mname=dict['mname'],
            director=dict['director'],
            actor=dict['actor'],
            time=dict['time'],
            type=dict['type'],
            online=dict['online'],
            offline=dict['offline'],
        )
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(type(e))
        if type(e) == IntegrityError:
            response['error_num'] = 2
        else:
            response['error_num'] = 1
        response['msg'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def delete_movie(request):
    print("method: delete movie")
    response = {}
    dict = json.loads(request.body)
    try:
        m = models.Movie.objects.get(mname=dict['last_name'])
        m.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        if type(e) == ProtectedError:
            response['error_num'] = 2
        else:
            response['error_num'] = 1
        response['msg'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def show_scene(request):
    print("method: show scene")
    response = {}
    dict = {}
    try:
        scene = models.All_scene.objects.filter()
        scene = json.loads(serializers.serialize("json", scene))
        cinema = models.Cinema.objects.filter()
        cinema = json.loads(serializers.serialize("json", cinema))
        for item in cinema:
            dict[item['pk']] = []
        for item in scene:
            item['fields']['sno'] = item['pk']
            dict[item['fields']['cno']].append(item['fields'])
        for item in cinema:
            item['fields']['scene'] = dict[item['pk']]
        response['list'] = cinema
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def delete_scene(request):
    print("method: delete scene")
    response = {}
    dict = json.loads(request.body)
    print(dict)
    try:
        m = models.Scene.objects.get(sno=dict['last_pk'])
        m.delete()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['error_num'] = 1
        response['msg'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def show_hall_movie(request):
    print("method: show scene")
    get = json.loads(request.body)
    response = {}
    c_list = []
    try:
        cinema = models.Cinema.objects.filter()
        cinema = json.loads(serializers.serialize("json", cinema))
        hall = models.Hall.objects.filter()
        hall = json.loads(serializers.serialize("json", hall))
        movie = models.Movie.objects.filter(online__lt=get['curDate'], offline__gt=get['curDate'])
        movie = json.loads(serializers.serialize("json", movie))
        for item in movie:
            item['fields']['mno'] = item['pk']
        for item in cinema:
            item['fields']['cno'] = item['pk']
            item['fields']['hall'] = []
            c_list.append(item['fields'])
        for item in hall:
            item['fields']['hno'] = item['pk']
            for item2 in c_list:
                if item2['cno'] == item['fields']['cno']:
                    item2['hall'].append(item['fields'])
                    break
        response['clist'] = c_list
        response['mlist'] = movie
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def insert_scene(request):
    print("method: insert scene")
    response = {}
    dict = json.loads(request.body)
    print("insert scene")
    try:
        c = models.Cinema.objects.get(cno=dict['cno'])
        h = models.Hall.objects.get(hno=dict['hno'])
        m = models.Movie.objects.get(mno=dict['mno'])
        models.Scene.objects.create(
            cno=c,
            hno=h,
            mno=m,
            ontime=dict['ontime'],
            offtime=dict['offtime'],
            price=dict['price']
        )
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        print(type(e))
        if type(e) == IntegrityError:
            response['error_num'] = 2
        else:
            response['error_num'] = 1
        response['msg'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def update_scene(request):
    print("method: update scene")
    response = {}
    dict = json.loads(request.body)
    try:
        c = models.Cinema.objects.get(cno=dict['cno'])
        h = models.Hall.objects.get(hno=dict['hno'])
        m = models.Movie.objects.get(mno=dict['mno'])
        s = models.Scene.objects.get(sno=dict['last_pk'])
        s.hno = h
        s.cno = c
        s.mno = m
        s.price = dict['price']
        s.ontime = dict['ontime']
        s.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['error_num'] = 1
        response['msg'] = str(e)
    return JsonResponse(response)