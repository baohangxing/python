# -*- coding: utf-8 -*-
# __author__ = 'H1MPLE'
# __link__ = 'https://github.com/baohangxing/python'
import os


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


class FileRW:
    def __init__(self, baseLocalName, ):
        # base链接地址
        mkpath = ".\\..\\..\\" + baseLocalName
        mkdir(mkpath)
        self.baseLocalName = mkpath + '\\'

    def write(self, fileName="fileName", content="", fileType="txt"):
        fileUrl = self.baseLocalName + fileName + "." + fileType
        self.checkFileExists(fileUrl)
        with open(fileUrl, 'a', encoding='utf-8') as f:
            f.write(content)
            f.close()

    @staticmethod
    def checkFileExists(fileUrl):
        if not os.path.exists(fileUrl):
            with open(fileUrl, 'w+', encoding='utf-8') as f:
                f.write('')
                f.close()
            return False
        return True
