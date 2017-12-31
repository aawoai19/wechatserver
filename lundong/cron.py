#!/usr/bin/python
#coding=utf-8

from lundong.get_value import sel_value

def run_get_value():
    try:
        value = sel_value()
        value.get_all()
        print 'done!'
    except:
        print 'wrong!'