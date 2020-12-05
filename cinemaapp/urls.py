from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'show_movie$', views.show_movie),
    url(r'login$', views.login)
]