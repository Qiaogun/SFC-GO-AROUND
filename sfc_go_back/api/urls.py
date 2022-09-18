from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/m5env3', views.get_env3json, name='get_env3json'),
    path('/m5heartrate', views.get_heartratejson, name='get_heartratejson'),
]