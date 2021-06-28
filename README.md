# 泛微OA漏洞合集

##### 当前集合漏洞：

```
泛微云桥任意文件读取

泛微OA V8前台Sql注入

泛微OA WorkflowServiceXml RCE CNVD-2019-32204

泛微OA weaver.common.Ctrl 任意文件上传

泛微OA Bsh RCE

泛微OA WorkflowCenterTreeData接口SQL注入(仅限oracle数据库) CNVD-2019-34241

泛微OA E-Cology 数据库配置信息泄漏
```
泛微OA V9 任意文件上传（未完成，测试ing）

先写了这些，也欢迎补充～

其中`/poc`下的利用脚本均可独立使用。

```bash
python3 poc.py url
```

##### Usage:

```bash
python3 main.py -f filename

python3 main.py -u url
```

![](https://zjun-info.oss-cn-chengdu.aliyuncs.com/zjun.info/image-20210628010147963.png)

![](https://zjun-info.oss-cn-chengdu.aliyuncs.com/zjun.info/image-20210628010645469.png)

## 参考

https://ailiqun.xyz/2021/05/02/%E6%B3%9B%E5%BE%AEOA-%E5%89%8D%E5%8F%B0GetShell%E5%A4%8D%E7%8E%B0/

http://wiki.peiqi.tech/

https://www.o2oxy.cn/3561.html

https://github.com/Henry4E36/weaverSQL

https://github.com/NS-Sp4ce/Weaver-OA-E-cology-Database-Leak


