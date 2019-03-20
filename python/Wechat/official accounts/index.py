
import os
import web
import time
import hashlib
import Control
from lxml import etree


urls = (
    '/weixin', 'WeixinInterface'
)


def _check_hash(data):
    # sha1加密算法
    signature = data.signature
    timestamp = data.timestamp
    nonce = data.nonce
    # 自己的token
    token = "123456789"  # 这里改写你在微信公众平台里输入的token
    # 字典序排序
    lis = [token, timestamp, nonce]
    lis.sort()
    sha1 = hashlib.sha1()
    #map(sha1.update, list)#python2使用
    list(map(sha1.update,[x.encode() for x in lis ]))#python3
    hashcode = sha1.hexdigest()
    # 如果是来自微信的请求，则回复True
    print(hashcode,signature)
    if hashcode == signature:
        return True
    return False


class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # 获取输入参数
        data = web.input()
        if _check_hash(data):
            return data.echostr

    def POST(self):
        str_xml = web.data()  # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        fromUser = xml.find("FromUserName").text
        content = xml.find("Content").text.strip()
        #content = xml.find("Content").text  # 获得用户所输入的内容
        msgType = xml.find("MsgType").text
        toUser = xml.find("ToUserName").text
        
        if msgType == 'text':
            ret = Control.analysis(content,fromUser)
            if ret:
                return self.render.reply_text(fromUser,toUser, int(time.time()), ret)
            else:
                return ""


application = web.application(urls, globals())
if __name__ == "__main__":
    application.run()
