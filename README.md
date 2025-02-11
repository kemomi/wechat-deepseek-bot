<!--
 * @Author: kemomi 
 * @Date: 2025-02-11 16:44:28
 * @LastEditors: mi zjm18702566651@163.com
 * @LastEditTime: 2025-02-11 21:48:02
 * @FilePath: \wechat-deepseek-bot\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# 微信 + DeepSeek AI 聊天机器人

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

基于企业微信的AI对话机器人，接入DeepSeek大模型API。

## 功能特性
-  ✅支持文本消息实时响应
-  ✅Docker一键部署
-  🔒HTTPS安全通信
-  🚥持Redis消息队列（可选）

## 快速部署

### 前置要求
- Linux服务器（推荐Ubuntu 22.04）
- Docker & Docker Compose
- 微信企业账号/个人账号

### 1. 克隆项目
```bash
git clone https://github.com/kemomi/wechat-deepseek-bot.git
cd wechat-deepseek-bot
```

### 2. 配置环境
```bash
cp config.yaml.example config.yaml
vim config.yaml  # 填写实际参数
```

### 3. 启动服务
```bash
docker-compose up -d --build
```

### 4. 验证部署
```bash
docker logs wechat-deepseek-bot_bot_1
```

## 高级配置
- **HTTPS设置**：编辑`deploy/nginx.conf`配置证书路径
- **性能优化**：启用Redis队列：
  ```yaml
  # docker-compose.yml
  depends_on:
    - redis
  ```

### **项目优化方向**
1. **消息持久化**：添加SQLite/MySQL存储对话记录
2. **多模型支持**：扩展兼容OpenAI/Claude等API
3. **管理后台**：使用FastAPI添加监控面板
4. **插件系统**：支持天气查询、新闻推送等扩展功能

---

### Docker部署
```bash
# 首次部署
docker-compose up -d --build

# 更新代码后
docker-compose restart bot
```


## 注意事项
1. 个人微信方案需自行承担封号风险
2. API调用频率限制建议：<5次/秒
3. 生产环境务必开启HTTPS


# 以下是搭建个人微信聊天机器人并接入DeepSeek API的分步指南，包含注意事项和优化建议：

---

### **一、准备工作**
1. **云服务器配置**
   - 系统推荐：Ubuntu 22.04 LTS（或其他Linux发行版）
   - 开放端口：确保开启`80`/`443`（HTTP/HTTPS）`22`（SSH）及微信回调端口（如有）

    *初始化虚拟环境*
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    ```

   - 安装依赖：
     ```bash
     sudo apt update && sudo apt install python3-pip nginx
     ```

2. **账号申请**
   - 获取DeepSeek API Key：访问[DeepSeek官网](https://platform.deepseek.com/)注册并获取API密钥。
     记录 API Endpoint 和 Key
   - 微信账号：建议使用**企业微信**（更稳定合法），个人号存在封号风险。

---

### **二、选择微信机器人框架**
#### 方案A：企业微信（推荐）
- **优势**：官方支持，稳定性高。
- **步骤**：
  1. 注册[企业微信](https://work.weixin.qq.com/)，创建应用获取`CorpID`、`AgentID`、`Secret`。
  2. 使用官方API或第三方库（如`wechatpy`）接收/发送消息。

#### 方案B：个人微信（高风险）
- **库选择**：`ItChat`（已停止维护）或逆向工程方案（如`wechaty-puppet-xp`）。
- **警告**：可能触发微信封禁，仅建议测试使用。

---

### **三、核心代码实现**
#### 1. 安装依赖
```bash
pip install requests wechatpy  # 企业微信方案
# 或
pip install requests itchat            # 个人微信方案（核心依赖）
```

#### 2. DeepSeek API调用示例
```python
import requests

def call_deepseek(api_key, prompt):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"请求出错：{str(e)}"
```

#### 3. 企业微信机器人示例（使用`wechatpy`）
```python
from wechatpy.enterprise import WeChatClient
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from flask import Flask, request, jsonify

app = Flask(__name__)
client = WeChatClient(corp_id='YOUR_CORPID', secret='YOUR_SECRET')

@app.route('/wechat', methods=['GET', 'POST'])
def handle_wechat():
    signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt = request.get_data()

    # 验证消息并解密
    try:
        crypto = WeChatCrypto('YOUR_TOKEN', 'YOUR_AES_KEY', 'YOUR_CORPID')
        decrypted = crypto.decrypt_message(encrypt, signature, timestamp, nonce)
    except InvalidSignatureException:
        return "Invalid Signature", 403

    # 处理消息
    msg = parse_message(decrypted)
    if msg.type == 'text':
        reply = call_deepseek('DEEPSEEK_API_KEY', msg.content)
        client.message.send_text(msg.agentid, msg.userid, reply)
    
    return "Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

---

### **四、部署与优化**
1. **安全配置**
   - 使用Nginx反向代理并配置HTTPS（Let's Encrypt免费证书）：
     ```bash
     sudo apt install certbot python3-certbot-nginx
     sudo certbot --nginx -d yourdomain.com
     ```
   - 敏感信息（API Key）通过环境变量传递，避免硬编码。

2. **性能优化**
   - 异步处理：使用`asyncio` + `aiohttp`提升并发能力。
   - 消息队列：对高并发场景，引入Redis队列缓冲请求。

3. **监控与日志**
   - 使用`supervisor`管理进程：
     ```ini
     [program:wechatbot]
     command=/usr/bin/python3 /path/to/bot.py
     autostart=true
     autorestart=true
     stderr_logfile=/var/log/wechatbot.err.log
     stdout_logfile=/var/log/wechatbot.out.log
     ```

---

### **五、注意事项**
1. **合规性**
   - 在微信消息处理逻辑中添加关键词过滤（如政治、暴力）。
   - 明确告知用户这是AI助手，回复可能存在误差。

2. **故障处理**
   - API调用失败时返回友好提示（如“服务繁忙，请稍后再试”）。
   - 设置速率限制（如`flask-limiter`）防止滥用。

3. **资源监控**
   - 使用`htop`或`glances`监控2G内存使用，避免OOM（内存溢出）。

---

### **六、完整架构图**
```
+-------------+     +-----------------+     +---------------+
| 微信用户端   | --> | 云服务器(Linux)  | --> | DeepSeek API  |
+-------------+     +-----------------+     +---------------+
                         | 处理逻辑：
                         | 1. 接收消息
                         | 2. 调用AI API
                         | 3. 返回响应
```

# 以下是搭建微信聊天机器人并部署到云服务器的详细流程及文件架构：

---

### 一、准备工作
1. **云服务器**
   - 购买云服务器（推荐腾讯云/阿里云/华为云）
   - 系统选择 Ubuntu 22.04 LTS
   - 开放安全组端口（SSH 22，HTTP 80/443）

2. **注册API**
   - 注册 [DeepSeek API](https://platform.deepseek.com/api) 获取 API Key
   - 记录 API Endpoint 和 Key

3. **开发环境**
   - 安装 VSCode
   - 安装 Python 3.10+ 和 Git

---

### 二、项目开发流程

#### 1. 创建项目目录
```bash
wechat-bot-deepseek/
├── config/
│   └── config.py          # 配置文件
├── src/
│   ├── bot.py             # 主程序逻辑
│   ├── deepseek_api.py    # API调用模块
│   └── wechat_handler.py  # 微信消息处理
├── requirements.txt       # 依赖列表
├── .gitignore             # 忽略文件
└── README.md              # 项目说明
```

#### 2. 初始化虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

#### 3. 安装依赖
```bash
pip install requests itchat  # 核心依赖
```

#### 4. 关键代码实现



#### 5. 测试本地运行
```bash
python src/bot.py
# 扫描控制台输出的二维码登录微信
```

---

### 三、部署到云服务器

#### 1. 服务器初始化
```bash
ssh root@your_server_ip
apt update && apt upgrade -y
apt install python3 python3-pip git
```

#### 2. 克隆代码
```bash
git clone https://github.com/kemomi/wechat-deepseek-bot.git
cd wechat-deepseek-bot
pip install -r requirements.txt
```

#### 3. 后台运行（使用nohup）
```bash
nohup python3 src/bot.py > bot.log 2>&1 &
```

---

### 四、高级配置建议
1. **进程守护**
   - 使用 `supervisor` 管理进程
   ```conf
   [program:wechat-bot]
   command=/path/to/venv/bin/python src/bot.py
   directory=/path/to/project
   autostart=true
   autorestart=true
   ```

2. **日志管理**
   - 添加日志轮转（logrotate）

3. **安全建议**
   - 使用微信小号测试
   - 配置服务器防火墙
   - API Key 通过环境变量传递

---

### 常见问题排查
1. 登录二维码显示问题：通过 `itchat.auto_login(enableCmdQR=True)` 启用终端二维码
2. API调用失败：检查网络连通性和API Key权限
3. 消息无响应：检查微信账号是否被风控

实际部署时需根据具体API文档调整参数，完整代码建议参考 [DeepSeek API文档](https://platform.deepseek.com/api-docs)。
