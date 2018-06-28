# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import rsa
#加密解密部分
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')


from django.shortcuts import render
from models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import game.views as gv
# from game.views import relate
from django.contrib.auth.hashers import make_password, check_password





def online_page(request):
    # return render(request, 'tem2/index.html')
    return render(request,'online/index.html')

def login_success(request, user_id):
    pc = prpcrypt('keyskeyskeyskeys')
    cryed_user_id = pc.encrypt(str(user_id))
    return gv.game_view(request,cryed_user_id)


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

    return render(request,'online/register_page.html')

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
        return HttpResponseRedirect(reverse('backEnd:online_page'))

# def logout(request,user_id):
#     _user = User.objects.get(user_id=user_id)
#     _user.online = False
#     _user.save()
#     return HttpResponseRedirect(reverse('backEnd:online_page'))

def logout(request,cryed_user_id):
    pc = prpcrypt('keyskeyskeyskeys')  # 初始化密钥
    user_id = int(pc.decrypt(cryed_user_id))
    _user = User.objects.get(user_id=user_id)
    _user.online = False
    _user.save()
    return HttpResponseRedirect(reverse('backEnd:online_page'))



def refresh_data(request,key):
    # #clear score data with the url: localhost/clear_score/382b493f0c0d801f2b0d3701e15ae2b3
    pc = prpcrypt('keyskeyskeyskeys')  # 初始化密钥
    # x = pc.decrypt(key)
    return HttpResponse(pc.encrypt(str(1)))
    # if(x == 'password'):
    #     users = User.objects.all()
    #     for user in users:
    #         user.history_high = 0
    #         user.save()
    #     return HttpResponse('Cleared all scores.')






