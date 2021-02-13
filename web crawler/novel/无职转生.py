# -*- coding: utf-8 -*-
# __author__ = 'H1MPLE'
# __link__ = 'https://github.com/baohangxing/python'
import re

from crawler_utils.fileRW import FileRW
from crawler_utils.tool import Tool


# 单页数据
class Page:
    def __init__(self, pages, url, title):
        self.name = pages
        self.url = url
        self.title = title

    def print(self):
        print("name:", self.name, "url:", self.url, "title:", self.title)


# 爬虫类
class NovelCrawler:
    # 初始化，传入基地址
    def __init__(self, menuUrl, baseUrl):
        self.menuUrl = menuUrl
        self.baseUrl = baseUrl
        self.FileRW = FileRW("无职转生")
        # 每个章节的地址
        self.pagesList = {}

    def setMenu(self, index=1):
        # 构建URL
        url = self.menuUrl
        if not index == 1:
            url = url.split("index.")[0] + "index_" + str(index) + ".html"
        string = Tool.requestUrl(url)
        string = string.split("《无职转生~到了异世界就拿出真本事~》正文")[1]
        result = re.findall(r"<li><a href=\"/book/42662/(.*?)\">(.*?)</a></li>", string)
        if result:
            for i in result:
                if i[1] and i[1].find("第") != -1:
                    pages = i[1].split(" ")[0]
                    if pages not in self.pagesList.keys():
                        self.pagesList[pages] = []
                    newPage = Page(pages, self.baseUrl + i[0], i[1])
                    self.pagesList[pages].append(newPage)

    # 传入章节的地址，获取章节的内容
    def getPage(self, newPage=Page("", "", ""), page=1):
        # 构建URL
        url = ""
        if page == 1:
            url = newPage.url
        else:
            url += newPage.url.split(".html")[0] + "_" + str(page) + ".html"

        string = Tool.requestUrl(url)
        hasNext = False
        if string.find("html\">下一页</a>") != -1:
            hasNext = True
        # print(string)
        strings = re.findall(r"请耐心等待,并刷新页面。(.+)<br /><script language=\"javascript\"", string, re.I | re.S)
        string = ""

        if len(strings) >= 1:
            string = strings[0]

        string = re.sub("                        ", "", string)
        string = re.sub("</div>", "", string)
        string = re.sub("<br />", " ", string)
        string = re.sub("\u3000", "", string)
        string = re.sub("&nbsp;", "", string)
        string = re.sub("台版转自轻之国度  扫图(.+?)录入：(.+?) ", " ", string)
        string = re.sub("★★★", "\n", string)

        # print(string)
        self.FileRW.write(newPage.name, string)
        if hasNext:
            self.getPage(newPage, page + 1)

    def start(self):
        for index in range(1, 17):
            self.setMenu(index)
        allCount = 0
        for pages in self.pagesList.keys():
            for item in self.pagesList[pages]:
                allCount += 1
        try:
            print("该帖子共有" + str(len(self.pagesList.keys())) + "卷", str(allCount) + "个网页")
            for key in self.pagesList.keys():
                littleName = key
                start = 0
                for item in self.pagesList[key]:
                    self.FileRW.write(littleName, "\n\n\n" + item.title)
                    start += 1
                    print("正在写入" + item.title + "         " + str(start) + "/" + str(
                        len(self.pagesList[key])))
                    self.getPage(item, 1)
        # 出现写入异常
        except IOError as e:
            print("写入异常，原因" + e.message)
        finally:
            print("写入任务完成")


menuUrl = 'https://www.fyxfcw.com/book/42662/index.html'
baseUrl = 'https://www.fyxfcw.com/book/42662/'
novelCrawler = NovelCrawler(menuUrl, baseUrl)
novelCrawler.start()
