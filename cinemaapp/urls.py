from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'show_movie$', views.show_movie),
    url(r'login$', views.login),
    url(r'reg$', views.reg),
    url(r'show_vip$', views.show_vip),
    url(r'show_employee$', views.show_employee),
    url(r'update_movie$', views.update_movie),
    url(r'insert_movie$', views.insert_movie),
    url(r'delete_movie$', views.delete_movie),
    url(r'show_scene$', views.show_scene),
    url(r'insert_scene$', views.insert_scene),
    url(r'update_scene$', views.update_scene),
    url(r'show_hall_movie$', views.show_hall_movie),
    url(r'delete_scene$', views.delete_scene),
    url(r'vip_credit$', views.vip_credit),
    url(r'get_disabled$', views.get_disabled),
    url(r'add_ticket$', views.add_ticket),
    url(r'show_ticket$', views.show_ticket),
    url(r'ret_ticket$', views.ret_ticket),
    url(r'show_sou$', views.show_sou),
    url(r'buy_sou$', views.buy_sou),
    url(r'show_sousingle$', views.show_sousingle),
    url(r'ret_sou$', views.ret_sou),
    url(r'add_sou$', views.add_sou),
    url(r'update_sou$', views.update_sou),
    url(r'delete_sou$', views.delete_sou),
    url(r'show_bill$', views.show_bill),
    url(r'show_allbill$', views.show_allbill)
]