# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def online_page(request):
    # return render(request, 'tem2/index.html')
    return render(request,'online/index.html')



# def game_view(request):
#     data = {
#
#     }
#     return render(request, 'tinyHeart/../game/templates/tinyHeart.html', data)
#     # return render(request, '1.html', data)

def register_page(request):
    data = {
        # 'type_list': ['manager','waiter','cook'],
    }
    return render(request,'online/register_page.html',data)

def register(request):
    _username = request.POST.get('username')
    _password = request.POST.get('password')
    _type = request.POST.get('type_')
    user_list = User.objects.filter(username=_username)
    #用户名是否存在
    if(len(user_list)>0):
        return HttpResponse('该用户名已存在！')
    else:
        new_user = User.objects.create(username=_username,password=_password,type=_type)
        ov.CURRENT_ID = new_user.user_id
        return HttpResponseRedirect(reverse('online:online_page'))