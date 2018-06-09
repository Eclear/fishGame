from django.conf.urls import url,include
from django.contrib import admin
# from django.views.generic import redirect_to
from . import views

urlpatterns = [
    url(r'^$', views.game_view,name='game_view'),
]