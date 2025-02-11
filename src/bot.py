from wechat_handler import text_reply
import itchat

def run():
    itchat.auto_login(hotReload=True)
    itchat.run()

if __name__ == "__main__":
    run()