# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','username','password','online','history_high')
    list_filter = ('online','user_id')

admin.site.register(models.User,UserAdmin)