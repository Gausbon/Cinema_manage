from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'show_movie$', views.show_movie),
    url(r'login$', views.login),
    url(r'show_vip$', views.show_vip),
    url(r'show_employee$', views.show_employee),
    url(r'show_boss$', views.show_boss),
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
    url(r'add_ticket$', views.add_ticket)
]