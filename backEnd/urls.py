from django.conf.urls import url,include
from . import views

urlpatterns = [
    # url(r'^$',views.game_view,name='game_view'),
    url(r'^$', views.online_page,name='online_page'),
    url(r'^register/$', views.register_page,name='register_page'),
    url(r'^registeraction/$', views.register,name='register'),
    url(r'^login/$', views.login,name='login'),
    url(r'^loginsuccess/(?P<type_id>[0-9]+)$',views.login_success,name='login_success'),
    url(r'^logoutuser/(?P<user_id>[0-9]+)$', views.logout,name='logout_user'),
    url(r'^logoutuser/(.+)$', views.logout,name='logout_user1'),
]