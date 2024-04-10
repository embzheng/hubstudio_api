from my_logtool import log
import requests
from playwright.sync_api import Playwright, sync_playwright
import subprocess
import json
import time

# 接口文档 https://support.hubstudio.cn/0379/7beb/fbb0/1d9a

def open_hubstudio(path, port, appid, appsec, groupid):
    cmd = f"{path} --server_mode=http --http_port={port} --app_id={appid} --group_code={groupid} --app_secret={appsec}"    
    p = subprocess.Popen(cmd)
    print(p.returncode)    

# 新建一个窗口
class HubBrowser:
    def __init__(self, url, headers='', id="", proxy_type='', proxy_host='', proxy_port='', proxy_user='', proxy_pwd=''):
        self.url = url
        self.headers = headers
        self.id = id
        self.debugging_port = ""
        self.context = None
        # 代理
        if proxy_type == "socks5":
            self.proxy_type = "Socks5" # 不使用代理/Socks5
        else:
            self.proxy_type = "不使用代理"
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pwd = proxy_pwd
        self.proxy_ip = '' #需要chack agent 后获取   
            
    def open(self):
        url = f'{self.url}/api/v1/browser/start'  # 打开环境
        open_data = {"containerCode": self.id}   # 填写参数，环境id可从创建环境或环境列表接口获取
        open_res = requests.post(url, json=open_data).json()
        if open_res['code'] != 0:
            log.error('环境打开失败:%s' % open_res)
            return 0
        self.debugging_port = open_res['data']['debuggingPort']  # 获取调试端口
        return self.debugging_port
    
    def close(self):
        url = f'{self.url}/api/v1/browser/stop'  # 打开环境
        open_data = {"containerCode": self.id}   # 填写参数，环境id可从创建环境或环境列表接口获取
        open_res = requests.post(url, json=open_data).json()
        if open_res['code'] != 0:
            log.error('环境关闭失败:%s' % open_res)
            return False
        return True

    # 获取playwright浏览器会话
    def get_browser_context(self, playwright):
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{self.debugging_port}")
        self.context = browser.contexts[0]
        return self.context

    def create(self, name):
        url = f'{self.url}/api/v1/env/create'  # 打开环境
        open_data = {
            "containerName": name,
            "asDynamicType": 2,
            "proxyTypeName": self.proxy_type,
            "proxyServer": self.proxy_host,
            "proxyPort": self.proxy_port,
            "proxyAccount": self.proxy_user,
            "proxyPassword": self.proxy_pwd,
            "coreVersion":118,
            "advancedBo" : {
                "uaVersion":118,
                "uiLanguage":"en",
                "languages":["en", "en-US"]
                }                     
            }   # 填写参数，环境id可从创建环境或环境列表接口获取
        open_res = requests.post(url, json=open_data).json()
        if open_res['code'] != 0:
            log.error('创建环境列表失败:%s' % open_res)
            return False
        self.id = open_res['data']['containerCode']
        log.info(f"创建环境成功, 环境id:{self.id}")
        return True  
    
    def update_proxy(self):
        json_data = {
            "containerCode": int(self.id),         #int         
            "asDynamicType": 2,
            'proxyTypeName': self.proxy_type, # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
            'proxyServer': self.proxy_host,  # 代理主机
            'proxyPort': self.proxy_port,  # 代理端口
            'proxyAccount': self.proxy_user,  # 代理账号
            'proxyPassword': self.proxy_pwd
            }
        open_res = requests.post(f"{self.url}/api/v1/env/proxy/update",
                        data=json.dumps(json_data), headers=self.headers).json()
        if open_res['code'] != 0:         
            log.error('更新代理失败:%s' % open_res)
            return False
        log.info(f"更新代理为 {self.proxy_type} 成功")
        return True  


def open_baidu(browser_context):
    # 使用第一个标签页打开playwright官网
    page = browser_context.pages[0]
    page.goto("https://www.baidu.com")
    print(page.title())

    # 新建标签页
    new_page = browser_context.new_page()
    # 打开百度
    new_page.goto("https://www.baidu.com")
    print(new_page.title())
    # 输入hubstudio并搜索
    new_page.fill('input[name="wd"]', 'hubstudio')
    new_page.press('input[id="su"]', 'Enter')

def list_browser():
    url = f'{myconfig.BROWSER_URL}/api/v1/env/list'  
    open_data = {"current": 1, "size":200}   # 填写参数，环境id可从创建环境或环境列表接口获取
    open_res = requests.post(url, json=open_data).json()
    if open_res['code'] != 0:
        log.error('获取环境列表失败:%s' % open_res)
        return None
    li = open_res['data']['list']
    return li  

def creat_browser(count=1):
    for i in range(count):   
            
        b = HubBrowser(url=myconfig.BROWSER_URL,
                    proxy_type=myconfig.PROXY_TYPE,
                    proxy_host=myconfig.PROXY_SERVER,
                    proxy_port=myconfig.PROXY_PORT,
                    proxy_user=proxy_user,
                    proxy_pwd=myconfig.PROXY_PWD)
        b.create(f"b{i}")
    

def update_browser_proxy(id):    
    
    b = HubBrowser(
                id=str(id),
                url=myconfig.BROWSER_URL,
                proxy_type=myconfig.PROXY_TYPE,
                proxy_host=myconfig.PROXY_SERVER,
                proxy_port=myconfig.PROXY_PORT,
                proxy_user=myconfig.proxy_user,
                proxy_pwd=myconfig.PROXY_PWD)
    b.update_proxy()

def login_browser(url, appid, appsec, groupid):
    url = f'{url}/login'  # 打开环境
    open_data = {
        "appId": appid,
        "appSecret": appsec,
        "groupCode": groupid,
        }   # 填写参数，环境id可从创建环境或环境列表接口获取
    open_res = requests.post(url, json=open_data).json()
    if open_res['code'] != 0:
        log.error('登录失败:%s' % open_res)
        return False
    log.info("登录成功")
    return True    


if __name__ == '__main__':
    
    
    ret = open_hubstudio("your hubstudio_connector.exe path", "6873")
    if ret == False:
        print("open browser err")    

    creat_browser()

    login_browser("http://127.0.0.1:6873", "your appid", "your appsec", "your groupid")
    
    li = list_browser()
    for b in li:
        id = b["containerCode"]
        update_browser_proxy(id)
    b = HubBrowser(url="http://127.0.0.1:6873",
                    headers={'Content-Type': 'application/json'},
                    id="567485568") 

    # 获取playwright浏览器会话
    with sync_playwright() as playwright:  
        b.open()    
        browser_context = b.get_browser_context(playwright)  # 填写环境的debuggingPort参数
        # 运行脚本
        open_baidu(browser_context)
        time.sleep(200)
