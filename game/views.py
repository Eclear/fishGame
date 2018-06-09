# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render


def game_view(request):
    data = {

    }
    return render(request, 'tinyHeart.html', data)
