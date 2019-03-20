# 导入模块

import os

from wxpy import *

import control

control.init()

# 初始化机器人，扫码登陆
if os.name == "nt":
    bot = Bot(cache_path=True)
else:
    while True:
        sel = input("please select:\n1:cmd\n2:shell\ninpurt number:")
        if sel.isdigit() and int(sel) in [1, 2]:
            break
        else:
            print("input error")
            continue
    bot = Bot(console_qr=sel, cache_path=True)

bot.enable_puid()

@bot.register(Friend, TEXT)
def auto_reply(msg):
    fromUserPuid = msg.sender.puid
    text = msg.text.strip()
    
    return control.analysis(text, fromUserPuid)

embed()
