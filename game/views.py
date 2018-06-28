# -*- coding: utf-8 -*-



from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
# from backEnd.views import prpcrypt
import json

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

from django.shortcuts import render
from backEnd.models import User


def relate(id1,id2):
    player1 = User.objects.get(user_id=id1)
    player2 = User.objects.get(user_id=id2)
    player1.friends.add(player2)
    player2.friends.add(player1)
    player1.save()
    player2.save()

def add_friend(request):
    id1 = request.GET['id1']
    id2 = request.GET['id2']
    id1 = int(id1)
    id2 = int(id2)
    player1 = User.objects.get(user_id=id1)
    # player2 = User.objects.get(user_name=name2)
    player2s = User.objects.filter(user_id=id2)
    if(len(player2s)>0):
        player2 = player2s[0]
        player1.friends.add(player2)
        player2.friends.add(player1)
        player1.save()
        player2.save()
        return HttpResponse("successfully add friend: "+player2.username)
    else:
        return HttpResponse("failed to add friend: "+str(id2)+",   typed a wrong user id")


def del_friend(request,id1,id2):
    player1 = User.objects.get(user_id=id1)
    player2 = User.objects.get(user_id=id2)
    player1.friends.remove(player2)
    player2.friends.remove(player1)
    player1.save()
    player2.save()
    return HttpResponseRedirect(reverse('game:friend_list', args=(id1,)))

def empty_data():
    for player in User.objects.all():
        player.history_high = 0
        player.save()

def game_view(request, cryed_user_id):
    # add_friend(1,3)
    pc = prpcrypt('keyskeyskeyskeys')
    user_id = int(pc.decrypt(cryed_user_id))
    player = User.objects.get(user_id = user_id)
    high = player.history_high
    friends = player.friends.all().order_by('history_high')
    pc = prpcrypt('keyskeyskeyskeys')
    # friends = User.objects.all()
    data = {
        'history_high': json.dumps(high),
        'friends': friends,
        'user_id':json.dumps(int(user_id)),
        'cryed_user_id':cryed_user_id,
    }
    # return render(request, 'tinyHeart.html', data)
    return render(request, 'gamer_main.html', data)

def friend_list(request, cryed_user_id):
    pc = prpcrypt('keyskeyskeyskeys')
    user_id = int(pc.decrypt(cryed_user_id))
    player = User.objects.get(user_id=user_id)
    high = player.history_high
    friends = player.friends.all().order_by('-history_high') #reversal
    data = {
        'history_high': json.dumps(high),
        'friends': friends,
        'user_id': json.dumps(int(user_id)),
        'i_user_id':int(user_id),
        'cryed_user_id': cryed_user_id,
    }
    return render(request, 'friend_list.html', data)


def update_data(request):
    new_score = int(request.GET['new_score'])
    id = int(request.GET['id'])
    player = User.objects.get(user_id=id)
    player.history_high = new_score
    player.save()
    return HttpResponse()

