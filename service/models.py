# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class userdialog(models.Model):
    userid = models.CharField(max_length=50)
    lasttime = models.IntegerField()
    tulingflag = models.IntegerField()
    jokingstep = models.IntegerField()

    def __unicode__(self):
        return self.userid