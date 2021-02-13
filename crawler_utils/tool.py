# -*- coding: utf-8 -*-
# __author__ = 'H1MPLE'
# __link__ = 'https://github.com/baohangxing/python'
import urllib.request


class Tool:
    def __init__(self):
        return

    @staticmethod
    def requestUrl(url, charset="utf-8"):
        try:
            print(url)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # 返回UTF-8格式编码内容
            string = str(response.read().decode(charset))
            return string
        except urllib.request.URLError as e:
            if hasattr(e, "reason"):
                if e.reason.find("Time-out") != -1:
                    print("连接失败,错误原因 超时重新连接，重新获取中")
                    return Tool.requestUrl(url, charset)
                else:
                    print(u"连接失败,错误原因", e.reason)
                    return ""
