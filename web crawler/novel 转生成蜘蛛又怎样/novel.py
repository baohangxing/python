# -*- coding: utf-8 -*-
# __author__ = 'H1MPLE'
# __link__ = 'https://github.com/baohangxing/python'
import urllib.request
import re


class TxtWriter:
    # 初始化，传入名字
    def __init__(self, name, ):
        # base链接地址
        self.name = '.\\' + name + ".txt"
        self.init()

    def init(self):
        with open(self.name, 'w', encoding='utf-8') as f:
            f.write('')
            f.close()

    def addWrite(self, string):
        with open(self.name, 'a', encoding='utf-8') as f:
            f.write(string)
            f.close()


# 爬虫类
class NovelCrawler:
    # 初始化，传入基地址
    def __init__(self, baseUrl, addWrite):
        # base链接地址
        self.baseURL = baseUrl

        self.addWrite = addWrite
        # 每个章节的地址
        self.pagesList = []

    # 获取所有的章节内容
    def setMenu(self):
        try:
            # 构建URL
            url = self.baseURL
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # 返回UTF-8格式编码内容
            string = str(response.read().decode("utf-8", "ignore"))
            result = re.findall(r"<li><a href=\"/book/.+\">", string)
            if result:
                for i in result:
                    page = re.findall(r"\d{7,8}.html", i)
                    if len(page) >= 1:
                        self.pagesList.append(page[0])
        # 无法连接，报错
        except urllib.request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接失败,错误原因", e.reason)
                return None

    # 传入章节的地址，获取章节的内容
    def getPage(self, pageUrl):
        try:
            # 构建URL
            url = self.baseURL + '/' + pageUrl
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # 返回UTF-8格式编码内容
            string = response.read().decode("gbk")
            titles = re.findall(r"<h1>.+</h1>", string)
            if len(titles) >= 1:
                title = titles[0]
                title = re.sub("<h1>", "\n", title)
                title = re.sub("</h1>", "", title)
                self.addWrite(title)
            result = re.findall(r"<p>.+</p>", string)
            allS = ""
            for i in result:
                item = i
                item = re.sub("<p>", "", item)
                item = re.sub("</p>", "\n", item)
                item = re.sub("铅笔小说", "\n", item)
                if item.find("（继续下一页）") == -1:
                    allS += item
            self.addWrite(allS)

        # 无法连接，报错
        except urllib.request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接失败,错误原因", e.reason)
                return None

    def start(self):
        self.setMenu()
        try:
            print("该帖子共有" + str(len(self.pagesList)) + "章节")
            for i in range(6, 10):
                print("正在写入 " + self.pagesList[i])
                self.getPage(self.pagesList[i])
        # 出现写入异常
        except IOError as e:
            print("写入异常，原因" + e.message)
        finally:
            print("写入任务完成")


txtWriter = TxtWriter("转生成蜘蛛又怎样")

menuUrl = 'https://www.x23qb.com/book/5999/'
novelCrawler = NovelCrawler(menuUrl, txtWriter.addWrite)
novelCrawler.start()
