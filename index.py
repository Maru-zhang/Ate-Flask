# -*- coding: UTF-8 -*-
from flask import Flask,render_template,request,make_response
import time
import hashlib
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont

app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def wechat_auth():
    if request.method == 'GET':
        if len(request.args) > 3:
            token = 'zhangbinhui'
            query = request.args
            signature = query['signature']
            timestamp = query['timestamp']
            nonce = query['nonce']
            echostr = query['echostr']
            s = [timestamp, nonce, token]
            s.sort()
            s = ''.join(s)
            sha1str = hashlib.sha1(s).hexdigest()
            if sha1str == signature:
                return make_response(echostr)
            else:
                return make_response("认证失败")
        else:
            return "认证失败"
    else:
        rec=request.stream.read()
        xml_rec=ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu,tou,str(int(time.time())),"哈哈哈哈"))
        response.content_type='application/xml'
        return response

@app.route("/test",methods = ["GET"])
def test():
    ttfont = ImageFont.truetype("/Library/Fonts/AppleGothic.ttf",20)
    im = Image.open("image.png")  
    draw = ImageDraw.Draw(im)  
    draw.text((100,10),u'I am a girl.', fill=(0,0,0),font=ttfont)  
    draw.text((40,40),unicode('hahahahha','utf-8'), fill=(0,0,0),font=ttfont)  
    # im.show() 
    im.save("./newImage.png")
    return "success" 