from django.core.management.base import BaseCommand, CommandError
from django.db import models
from lundong.get_value import sel_value
import os
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(3):
            print time.ctime(time.time())
            try:
                value = sel_value()
                value.get_all()
                print 'done!'
                break
            except:
                print 'wrong!'
            finally:
                value.close()