# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
import json

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

def game_view(request, user_id):
    # add_friend(1,3)
    player = User.objects.get(user_id = user_id)
    high = player.history_high
    friends = player.friends.all().order_by('history_high')

    # friends = User.objects.all()
    data = {
        'history_high': json.dumps(high),
        'friends': friends,
        'user_id':json.dumps(int(user_id)),
    }
    # return render(request, 'tinyHeart.html', data)
    return render(request, 'gamer_main.html', data)

def friend_list(request, user_id):
    player = User.objects.get(user_id=user_id)
    high = player.history_high
    friends = player.friends.all().order_by('-history_high') #reversal
    data = {
        'history_high': json.dumps(high),
        'friends': friends,
        'user_id': json.dumps(int(user_id)),
        'i_user_id':int(user_id),
    }
    return render(request, 'friend_list.html', data)


def update_data(request):
    new_score = int(request.GET['new_score'])
    id = int(request.GET['id'])
    player = User.objects.get(user_id=id)
    player.history_high = new_score
    player.save()
    return HttpResponse()
