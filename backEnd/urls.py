from django.conf.urls import url,include
from . import views

urlpatterns = [
    # url(r'^$',views.game_view,name='game_view'),
    url(r'^$', views.online_page,name='online_page'),
    url(r'^register/$', views.register_page,name='register_page'),
    url(r'^registeraction/$', views.register,name='register'),
]