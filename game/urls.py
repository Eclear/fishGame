from django.conf.urls import url,include
from django.contrib import admin
# from django.views.generic import redirect_to
from . import views

urlpatterns = [
    # url(r'^$', views.game_view,name='game_view'),
    url(r'^/(?P<user_id>[0-9]+)$', views.game_view,name='game_view'),
    # url(r'^friends/(?P<user_id>[0-9]+)$', views.friend_list,name='friend_list'),
    url(r'^friends/(.+)$', views.friend_list,name='friend_list1'),
    # url(r'^id=(?:id-(?P<user_id>[0-9]+)/)?$', views.game_view,name='game_view'),
    url(r'^del_friend/(?P<id1>[0-9]+)/(?P<id2>[0-9]+)$', views.del_friend,
        name='del_friend'),

]