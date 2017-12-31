# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from service.models import userdialog
import time
from service.tuling import sendtuling

WECHAT_TOKEN = 'mahhhraspberrypi'
AppID = 'wx0a69695d0ecfc941'
AppSecret = ''

# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)


@csrf_exempt
def index(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
    # 获取来源用户OpenID
    userid = message.source
    # 会话超时判断
    userid = str(userid)
    try:
        dialog = userdialog.objects.get(userid=userid)
    except:
        dialog = userdialog.objects.create(userid = userid,lasttime = int(time.time()),tulingflag = 0,jokingstep = 0)
    if (int(time.time()) - dialog.lasttime) > 180:
        dialog.tulingflag = 0
        dialog.jokingstep = 0
    else:
        pass
    response = None
    # 关注事件的默认回复
    if message.type == 'subscribe':
        response = wechat_instance.response_text(
            content=(
                '感谢您的关注！\n回复【功能】两个字查看支持的功能'
            ))
    # 文字内容的回复
    elif isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
        reply_text = (
            '好委屈，我没有听懂哦😝'
        )
        if dialog.tulingflag == 1:
            if content == '退出':
                dialog.tulingflag = 0
                reply_text = (
                    '已退出聊天模式'
                )
            else:
                tuling_chat = sendtuling(content,str(userid))
                reply_text = (
                    tuling_chat
                )
        else:
            if content == '功能':
                reply_text = (
                    '目前支持的功能：\n1、回复【二八轮动】可以搜索数据，查看最新指数情况\n'
                    '2、回复【陪我聊天】，查天气，陪聊天，讲故事，你的小伙伴【小小某】无所不能！'
                    '还有更多好玩和实用的功能正在开发中哦 ^_^'
                    # '\n【<a href="https://www.mahhh.imwork.net">马某个人主页</a>】'
                )
            elif content == '二八轮动':
                reply_text = (
                    '实时观测深沪300指数与创业板指数变化\n'
                    '还有更多好玩和实用的功能正在开发中哦 ^_^\n'
                    '【<a href="http://www.mahh.xin/lundong">点我查看</a>】'
                    '\n【<a href="http://39.106.8.229/lundong">备用地址</a>】'
                    # '\n【<a href="https://www.douban.com/note/551791040/">了解更多</a>】'
                )
            elif content == '陪我聊天':
                dialog.tulingflag = 1
                reply_text = (
                    '人工智能的【小小某】已开启陪聊模式😎'
                    '\n如果您想要退出聊天模式，请回复【退出】'
                    '\n(本功能基于<a href="http://www.tuling123.com/">图灵机器人</a>开发)'
                    '\n还有更多好玩和实用的功能正在开发中哦 ^_^'
                )
            else:
                tuling_chat = sendtuling(content, str(userid))
                reply_text = (
                    tuling_chat
                )

        # elif content.endswith('教程'):
        #     reply_text = '您要找的教程如下：'

        response = wechat_instance.response_text(content=reply_text)
    # 非文字内容回复
    else:
        response = wechat_instance.response_text(
            content=(
                '哎呀，我现在只会读文字啊😥'
            )
        )
    dialog.lasttime = int(time.time())
    dialog.save()
    return HttpResponse(response, content_type="application/xml")
