from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=30)
    role = models.BooleanField()

    def __unicode__(self):
        return self.role


class LoginUser(models.Model):
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name