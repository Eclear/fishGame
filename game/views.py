# -*- coding: utf-8 -*-



from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
import json

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')


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
        if player2 in player1.friends.all():
            return HttpResponse("friend already exists")
        player1.friends.add(player2)
        player2.friends.add(player1)
        player1.save()
        player2.save()
        return HttpResponse("successfully added friend: "+player2.username)
    else:
        return HttpResponse("failed to add friend: "+str(id2)+",   typed a wrong user id")


# def del_friend(request,id2,cryed_id1):
#     pc = prpcrypt('keyskeyskeyskeys')
#     id1 = int(pc.decrypt(cryed_id1))
#     player1 = User.objects.get(user_id=id1)
#     player2 = User.objects.get(user_id=id2)
#     player1.friends.remove(player2)
#     player2.friends.remove(player1)
#     player1.save()
#     player2.save()
#     return HttpResponseRedirect(reverse('game:friend_list1', args=(pc.encrypt(id1),)))

def del_friend(request):
    cryed_id1 = request.GET.get('p1')
    id2 = request.GET.get('p2')
    pc = prpcrypt('keyskeyskeyskeys')
    id1 = int(pc.decrypt(cryed_id1))
    player1 = User.objects.get(user_id=id1)
    player2 = User.objects.get(user_id=id2)
    player1.friends.remove(player2)
    player2.friends.remove(player1)
    player1.save()
    player2.save()
    return HttpResponseRedirect(reverse('game:friend_list1', args=(cryed_id1,)))

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

