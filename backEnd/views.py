# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import game.views as gv

def online_page(request):
    # return render(request, 'tem2/index.html')
    return render(request,'online/index.html')

def login_success(request, user_id):
    return gv.game_view(request,user_id)


def login(request):
    _username = request.POST.get('username')
    _password = request.POST.get('password')
    user_list = User.objects.filter(username=_username,password=_password)
    #确定登录是否成功
    if(len(user_list)==0):
        return HttpResponse('请输入正确的用户名和密码')
    else:
        _user = user_list[0]
        _user.online = True
        _user.save()
        request.session['member_id'] = _user.user_id
        return login_success(request, _user.user_id)

def register_page(request):
    data = {
        'type_list': ['manager','waiter','cook'],
    }
    return render(request,'online/register_page.html',data)

def register(request):
    _username = request.POST.get('username')
    _password = request.POST.get('password')
    # _type = request.POST.get('type_')
    user_list = User.objects.filter(username=_username)
    #用户名是否存在
    if(len(user_list)>0):
        return HttpResponse('该用户名已存在！')
    else:
        new_user = User.objects.create(username=_username,password=_password)
        gv.relate(new_user.user_id, new_user.user_id)
        gv.CURRENT_ID = new_user.user_id
        return HttpResponseRedirect(reverse('backEnd:online_page'))

def logout(request,user_id):
    _user = User.objects.get(user_id=user_id)
    _user.online = False
    _user.save()
    return HttpResponseRedirect(reverse('backEnd:online_page'))



def refresh_data(request, system_key):  #
    if(system_key=='2587946'):
        users = User.objects.all()
        for user in users:
            user.history_high = 0
            user.save()
        return HttpResponse('Cleared all scores.')
    return HttpResponse('System key wrong')