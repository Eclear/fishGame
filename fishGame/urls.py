"""fishGame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import game.views as gv
import backEnd.views as bv


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('backEnd.urls',namespace='backEnd')),
    url(r'^game/', include('game.urls',namespace='game')),
    url(r'^add_friend/$', gv.add_friend, name='add'),
    url(r'^update_data/$', gv.update_data, name='add'),
    url(r'^clear_score/(?P<system_key>[0-9]+)$', bv.refresh_data,name='clear_score'),
]
