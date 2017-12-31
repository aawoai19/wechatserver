# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Zhishu(models.Model):
    name = models.CharField(max_length=10)
    name_id = models.BigIntegerField()
    idkey = models.IntegerField()
    value = models.FloatField()
    date = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name_id