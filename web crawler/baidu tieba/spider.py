# coding=utf-8
# __author__ = 'H1MPLE'
# __link__ = 'https://github.com/baohangxing/python'
import urllib.request
import re
import pandas as pd
import datetime


# 处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    # 帖子页数
    pagesNum = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
    # 分块的标志
    splitTag = re.compile("l_post l_post_bright j_l_post clearfix")
    # 内容提取
    contentTag = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
    # 时间和楼层提取
    infosTag = re.compile('<span class="tail-info"*?>(.*?)</span>', re.S)
    # id
    huyaIdTag = re.compile('[a-zA-Z0-9_]+', re.S)

    timeTag = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


# 百度贴吧爬虫类
class BDTB:
    # 初始化，传入基地址
    def __init__(self, baseUrl, ):
        # base链接地址
        self.baseURL = baseUrl
        # HTML标签剔除工具类对象
        self.tool = Tool()
        # 全局file变量，文件写入操作对象
        self.file = None
        # 楼层标号，初始为1
        self.floor = 1
        # 默认的标题
        self.defaultTitle = u"百度贴吧统计"

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageNum):
        try:
            # 构建URL
            url = self.baseURL + '?pn=' + str(pageNum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # 返回UTF-8格式编码内容
            return response.read().decode("utf-8")
        # 无法连接，报错
        except urllib.request.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接百度贴吧失败,错误原因", e.reason)
                return None

    # 获取帖子一共有多少页
    def getPageNum(self, page):
        # 获取帖子页数的正则表达式
        result = re.search(self.tool.pagesNum, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getFloorInfo(self, list):
        for i in list:
            if i.find("楼") != -1:
                return i
        return ''

    def getTimeInfo(self, list):
        for i in list:
            str = self.tool.timeTag.match(i)
            if str:
                return i
        return ""

    def getHuyaId(self, str):
        ids = re.findall(self.tool.huyaIdTag, str)
        if ids and len(ids) > 0 and len(ids[0]) > 1:
            return ids[0]
        return ''

    # 获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        # 匹配所有模块
        list = re.split(self.tool.splitTag, page)
        contents = []
        for item in list:
            items = re.findall(self.tool.contentTag, item)
            if items and len(items) > 0:
                # 将文本进行去除标签处理
                content = self.tool.replace(items[0])
                # 提取楼层和时间
                infos = re.findall(self.tool.infosTag, item)
                s = [self.floor, self.getFloorInfo(infos), self.getTimeInfo(infos), content, self.getHuyaId(content)]
                contents.append(s)
        return contents

    def getFileName(self):
        return self.defaultTitle + ".xlsx"

    def create_excel(self):
        file_path = self.getFileName()
        df = pd.DataFrame(columns=["页数", "楼层", "时间", "内容", "hy id提取"])
        df.to_excel(file_path, index=False)

    # 添加到后面
    def writeData(self, contents):
        df = pd.read_excel(self.getFileName(), header=None)
        df = df.append(contents, ignore_index=True)
        df.to_excel(self.getFileName(), index=False, header=False)
        self.floor += 1

    def start(self):
        self.create_excel()
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        if not pageNum:
            print("URL已失效，请重试")
            return
        try:
            print("该帖子共有" + str(pageNum) + "页")
            for i in range(1, int(pageNum) + 1):
                print("正在写入第" + str(i) + "页数据")
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        # 出现写入异常
        except IOError as e:
            print("写入异常，原因" + e.message)
        finally:
            print("写入任务完成")


baseURL = 'https://tieba.baidu.com/p/7179322924'
bdtb = BDTB(baseURL)
bdtb.start()
