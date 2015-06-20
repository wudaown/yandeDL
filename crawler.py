__author__ = 'wudaown'
# -*- coding: utf-8 -*-
import urllib
import urllib.request
import urllib.parse
import re
import os

###
### 所有正规则都是通过wget下载网页然后分析html得到
###
def createDir(dirName):
    if os.path.exists(dirName) == True:  # 创建对应的TAG文件夹
        print('文件夹已经存在 ！')
    else:
        os.mkdir(dirName)
    os.chdir(dirName)


def ask_tag():
    word = {}
    word['key'] = input("输入关键字： ")  # 用字典保存tag
    keyword = "?tags"
    url = "https://yande.re/post"
    search_word = urllib.parse.urlencode(word)  # parse tag形成网页需要的格式
    search_word = search_word[3:]
    full_url = url + keyword + search_word
    return full_url  # 返回对应的网页 url 后面会用到


def determineTag(full_url):  # 判断搜索的tag是否存在 并且做出相应措施
    url_html = getSource(full_url)  # 通过getSource把网页url变成html源码
    listTag = possibleTag(url_html)  # 通过possibleTag分析html源码判断tag是否存在
    if listTag == []:  # listTag存储网站提示的tag 如没有则代表搜索的tag存在
        createDir(full_url[27:])  # 建立文件夹
        return (url_html, full_url)  # 返回html源码以及相应的网页url 稍后用到
    else:
        count = 1
        total_tag = len(listTag)
        for x in listTag:
            print(count, x)  # 如listTag不是空的 则代表搜索的tag不存在
            count = count + 1  # 给每个建议的tag编号并且输出到屏幕
            if count > total_tag:
                break  # 想不到跳出循环的方法了 于是就break
        chooseTag = int(input('请输入要查找的TAG : '))
        suggest_url_tag = suggestTag(listTag, chooseTag - 1)  # 通过suggestTag返回建议的tag对应url 一共给了两个参数
        suggest_url_html = getSource(suggest_url_tag)  # 第二个参数因为index从0开始 所以-1
        createDir(suggest_url_tag[27:])
        return (suggest_url_html, suggest_url_tag)  # 同上返回需要的源码以及对应url


def suggestTag(listTag, choose):  # suggestTag函数返回建议的tag对应url
    """

    :rtype : str
    """
    url = 'https://yande.re/post'
    keyword = '?tags='
    suggest_url = url + keyword + listTag[choose]
    return suggest_url


def next_page(url_page, page_number):  # next_page函数分析当前网页url以便前往下一页
    page_number = page_number + 1  # 这里page_number变量默认在main函数默认为1
    next_page_url = url_page[0:22] + 'page=' + str(page_number) + '&' + url_page[22:]
    return (next_page_url, page_number)  # 这里返回下一页url以及页数 一共继续循环


def getSource(source):  # pass url得到网页html源码
    url = urllib.request.urlopen(source).read().decode('utf-8')
    return url


def possibleTag(link):  # possibleTag分析网页源码判断搜索tag是否存在
    possibletag = re.compile('Maybe you meant: <.*')
    findtag = re.compile('href="(.+?)"')  # 正则表达式提取内容
    tempTag = ''  # 这里说一下没有办法一次提取完 所以下面又提取了一次
    listTag = []
    if 'Nobody' in link:  # 主要判断语句 分析源码得到
        print('True')
        for x in possibletag.findall(link):
            tempTag = x
        for x in findtag.findall(tempTag):
            listTag.append(urllib.parse.unquote(x[11:]))
    return listTag


def extract_link(link):  # extract_link 函数提取每张图片单独的页面
    page = []
    elink = re.compile('https://yande.re/post/show/\d{6}')
    for x in elink.findall(link):
        page.append(x)
    return page

def getimgLink(url_html):
    dLink = []
    direct_link = re.compile('directlink \w{5}img"(.+?.jpg)')
    for x in direct_link.findall(url_html):
        dLink.append(x[7:])
    return dLink


# def imgLink(postlink):  # imgLink 函数通过正则表达式提取每张图片的直连 direct link
#     templink = []
#     plink = re.compile('src="https://files.yande.re\/.*.jpg')
#     for x in plink.findall(postlink):
#         templink.append(x[5:])
#     return templink


# def download_link(page):  # download_link 函数基本上封装了一下 相当于一个循环提取多个图片地址
#     dLink = []
#     for x in page:
#         dLink.append(str(imgLink(getSource(x))))
#     return dLink


def correct_filename(dLink):  # correct_filename 函数 读取图片直连 经过修改保留图片名字
    filename_list = []
    for x in dLink:  # 这里说一下 一开始通过正则表达式结果有部分图片直连不标准
        temp = urllib.request.unquote(x)  # 导致后面index out of range
        filename_list.append(temp[70:])  # 最后还是通过unquote
        # filename_list.append(temp[74:-2])  # 最后还是通过unquote
    return filename_list


def getImg(dLink, filename_list):  # getImg 函数负责下载图片并且判断图片是否存在
    count = 0
    for x in dLink:
        if os.path.exists(filename_list[count]) == False:
            urllib.request.urlretrieve(x, filename_list[count])
            # urllib.request.urlretrieve(x[2:-2], filename_list[count])
            print('下载第', count + 1, '张图片')
            print('下载中------------')
            print('下载中----------------')
            count = count + 1
        else:
            print('图片已经存在 ！')
