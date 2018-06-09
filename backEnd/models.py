# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    user_id = models.AutoField(auto_created=True,  primary_key=True,serialize=False, verbose_name='ID')
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    # type = models.CharField(max_length=25)
    online = models.BooleanField(default=False)
    history_high = models.IntegerField(default=0)
    friends = models.ManyToManyField('User',blank=True)
    def __unicode__(self):
        return self.username
    # coding:utf8
