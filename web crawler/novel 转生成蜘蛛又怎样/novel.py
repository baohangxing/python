# -*- coding: utf-8 -*-
# __author__ = 'H1MPLE'
# __link__ = 'https://github.com/baohangxing/python'
import time
import urllib.request
import re
import os


class TxtWriter:
    # 初始化，传入名字
    def __init__(self, name, ):
        # base链接地址
        self.name = '.\\' + name

    def write(self, littleName="", content=""):
        name = self.name + littleName + ".txt"
        with open(name, 'a', encoding='utf-8') as f:
            f.write(content)
            f.close()

    def cheakFileExists(self, littleName="", ):
        name = self.name + littleName + ".txt"
        if not os.path.exists(name):
            with open(name, 'w', encoding='utf-8') as f:
                f.write('')
                f.close()
            return False
        return True


# 爬虫类
class NovelCrawler:
    # 初始化，传入基地址
    def __init__(self, menuUrl, baseUrl):
        # base链接地址
        self.baseURL = baseUrl
        self.menuUrl = menuUrl
        self.txtWriter = TxtWriter("转生成蜘蛛又怎样")
        # 每个章节的地址
        self.pagesList = {}
        self.listIndex = []

    # 待优化
    def getNameFormChinese(self, string=""):
        arr = string.split(" ")
        value = ""
        if arr:
            value = arr[0]
        if value not in self.listIndex:
            self.listIndex.append(value)
            return "s" + str(len(self.listIndex))
        index = self.listIndex.index(value)
        return "s" + str(index + 1)

    def setMenu(self):
        try:
            # 构建URL
            url = self.menuUrl
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # 返回UTF-8格式编码内容
            string = str(response.read().decode("gbk"))
            result = re.findall(r"<li><a href=\"/book/(.+)\">(.+)</a></li>", string)
            if result:
                for i in result:
                    if i[1] and i[1].find("第") != -1:
                        key = self.getNameFormChinese(i[1])
                        if key not in self.pagesList.keys():
                            self.pagesList[key] = []
                        self.pagesList[key].append(i)
            print(self.pagesList)
        # 无法连接，报错
        except urllib.request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接失败,错误原因", e.reason)
                return None

    # 传入章节的地址，获取章节的内容
    def getPage(self, pageUrl, littleName, page=1):
        try:
            # 构建URL
            url = self.baseURL
            if page == 1:
                url += pageUrl
            else:
                url += pageUrl.split(".")[0] + "_" + str(page) + "." + pageUrl.split(".")[1]
            print(url)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # 返回UTF-8格式编码内容
            string = response.read().decode("gbk")
            titles = re.findall(r"<h1>.+</h1>", string)
            title = ""
            if len(titles) >= 1:
                title = titles[0]
                title = re.sub("<h1>", "\n", title)
                title = re.sub("</h1>", "", title)
                title += "\n"
            result = re.findall(r"<p>.+</p>", string)
            allS = ""
            next = False
            for i in result:
                if i.find("（继续下一页）") != -1:
                    next = True
                item = i
                item = re.sub("<p>", "", item)
                item = re.sub("</p>", "\n", item)
                item = re.sub("铅笔小说", "\n", item)
                item = re.sub("<p style=\"font-weight: 400;color:#af888c;\">（继续下一页）", "", item)
                allS += item
            self.txtWriter.write(littleName, title)
            self.txtWriter.write(littleName, allS)
            if next:
                self.getPage(pageUrl, littleName, page + 1)

                # 无法连接，报错
        except urllib.request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接失败,错误原因", e.reason)
                if e.reason.find("Time-out") != -1:
                    print("超时重新连接")
                    self.getPage(pageUrl, littleName, page)

    def start(self):
        self.setMenu()
        try:
            print("该帖子共有" + str(len(self.pagesList.keys())) + "卷")
            for key in self.pagesList.keys():
                littleName = key
                if self.txtWriter.cheakFileExists(littleName):
                    print(self.txtWriter.name + littleName + "已存在跳过")
                    continue
                for item in self.pagesList[key]:
                    self.txtWriter.write(littleName, item[1] + "\n")
                start = 0
                for item in self.pagesList[key]:
                    start += 1
                    print("正在写入" + item[1] + "         " + str(start) + "/" + str(len(self.pagesList[key])))
                    self.getPage(item[0], littleName, 1)

        # 出现写入异常
        except IOError as e:
            print("写入异常，原因" + e.message)
        finally:
            print("写入任务完成")


menuUrl = 'https://www.x23qb.com/book/5999/'
baseUrl = 'https://www.x23qb.com/book/'
novelCrawler = NovelCrawler(menuUrl, baseUrl)
novelCrawler.start()
