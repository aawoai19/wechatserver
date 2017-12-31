#!/usr/bin/python
#coding=utf-8

import requests
import json,re

class get_value():
    def __init__(self,num):
        self.num = num
        self.url = "http://fundgz.1234567.com.cn/js/%s.js"

    def getit(self):
        url = self.url%self.num
        response = requests.get(url,params=None).text
        j = json.loads(re.findall(r'^\w+\((.*)\);$', response)[0])
        return j

    def is_today(self):
        j = self.getit()
        gztime = j['gztime']
        return gztime[11:] == '15:00'