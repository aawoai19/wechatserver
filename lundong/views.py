# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from lundong.get_value import sel_value
from lundong.models import Zhishu
import json
from get_today_data import get_value

# Create your views here.
def get_value_test(request):
    value = sel_value()
    value.get_all()
    return HttpResponse(u'完成')

def lundong_list(request):
    data = {
        'sz50':[],
        'sh300':[],
        'zz500':[],
        'cyb':[]
    }
    sh300_Num = '002987'
    cyb_Num = '001593'
    sz50_Num = '001549'
    zz500_Num = '002903'
    f_dir = {
        'sz50': sz50_Num,
        'sh300': sh300_Num,
        'zz500': zz500_Num,
        'cyb': cyb_Num
    }
    for k,li in data.items():
        for i in range(40):
            value = Zhishu.objects.get(name=k,idkey=i+1).value
            value = round(value,4)
            li.append(value)
        data[k] = li
        it = get_value(f_dir[k])
        jdata= it.getit()
        get_date = jdata['gztime'][:10]
        if not get_date == Zhishu.objects.get(name=k,idkey=1).date:
            data[k].insert(0,round(float(jdata['gsz']),4))
    return HttpResponse(json.dumps(data),content_type='application/json')

def lundong(request):
    return render(request,'lundong.html')
