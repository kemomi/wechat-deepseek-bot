#!/bin/bash
###
 # @Author: kemomi
 # @Date: 2025-02-11 17:16:39
 # @LastEditors: kemomi 
 # @LastEditTime: 2025-02-11 17:19:47
 # @FilePath: \wechat-deepseek-bot\scripts\setup.sh
 # @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
### 

# 初始化环境
sudo apt update
sudo apt install -y python3-venv nginx supervisor

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置Nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/wechatbot
sudo ln -s /etc/nginx/sites-available/wechatbot /etc/nginx/sites-enabled/
sudo systemctl reload nginx

# 配置Supervisor
sudo cp deploy/supervisor.conf /etc/supervisor/conf.d/wechatbot.conf
sudo supervisorctl update

# 设置HTTPS（可选）
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com