'''
Author: kemomi 
Date: 2025-02-11 16:41:09
LastEditors: kemomi 
LastEditTime: 2025-02-11 18:30:19
FilePath: \wechat-deepseek-bot\src\deepseek_api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests
from config.config import DEEPSEEK_API_KEY, DEEPSEEK_ENDPOINT

def call_deepseek_api(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "deepseek-chat"
    }
    response = requests.post(DEEPSEEK_ENDPOINT, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]