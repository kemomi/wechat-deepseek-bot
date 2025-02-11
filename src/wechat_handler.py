'''
Author: kemomi 
Date: 2025-02-11 16:41:38
LastEditors: kemomi 
LastEditTime: 2025-02-11 18:56:37
FilePath: \wechat-deepseek-bot\src\wechat_handler.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import itchat
from deepseek_api import call_deepseek_api

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    user_input = msg['Text']
    reply = call_deepseek_api(user_input)
    return reply