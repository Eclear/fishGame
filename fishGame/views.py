# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def game_view(request):
    data = {

    }
    return render(request, 'tinyHeart/../game/templates/tinyHeart.html', data)
    # return render(request, '1.html', data)