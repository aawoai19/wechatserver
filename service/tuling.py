#coding=utf-8

import json
import requests
import urllib,urllib2
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def sendtuling(text,user):
    data = {
        'info':text,
        "key": "a2ba62a203ae49f389ace3a8da9e4352",
        "userid": user
    }
    headers = {'Content-Type': 'application/json','charset':'utf-8'}
    value = json.dumps(data)
    res = urllib2.Request(url="http://www.tuling123.com/openapi/api",data=value,headers=headers)
    response = urllib2.urlopen(res)
    re = response.read()
    re = json.loads(re)
    # res = requests.post(url='http://www.tuling123.com/openapi/api', headers=headers, data=json.dumps(data))
    # re = json.loads(res.text)
    if re['code'] == 100000:
        return re['text']
    elif re['code'] == 200000:
        return re['text']+'\n'+re['url']
    elif re['code'] == 302000:
        resp = ''
        for it in re['list']:
            resp += '<a href="'+ it['detailurl'] +'">'+ it["article"] + '</a>\n'
        return resp
    else:
        return re['text']
if __name__ == '__main__':
    tuling = sendtuling('啊啊啊','iopopfdf')
    print tuling.decode('utf-8')
    print tuling
    print {'黑猫警长！😂'}