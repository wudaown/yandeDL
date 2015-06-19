__author__ = 'wudaown'
# -*- coding: utf-8 -*-

import crawler
import urllib
import urllib.request
import re


def coreDL(html_url):  # coreDL 函数把crawler.py里的函数封装了一遍 把所有下载有关的函数封装了
    page = crawler.extract_link(html_url)
    dLink = crawler.download_link(page)
    filename_list = crawler.correct_filename(dLink)
    crawler.getImg(dLink, filename_list)
    print('下载完成 ！ ')


def MultiPageDownload():  # MultiPageDownload 函数负责一次下载多个页面
    total_number_of_page = int(input("请输入一共要下载页数 : "))
    current_page_number = 1  # 默认当前页数为1
    full_url = crawler.ask_tag()  # 询问tag
    current_page_html, current_page_url = crawler.determineTag(full_url)  # 判断tag是否存在
    while current_page_number < total_number_of_page:  # 多页面下载循环
        coreDL(current_page_html)
        (next_page_url, next_page_number) = crawler.next_page(current_page_url, current_page_number)
        current_page_number = current_page_number + 1
        coreDL(crawler.getSource(next_page_url))
    return True


def SinglePageDownload():  # SinglePageDownlaod 函数每次下载一页 完成后询问是否继续
    full_url = crawler.ask_tag()  # 同上询问tag
    current_page_html, current_page_url = crawler.determineTag(full_url)  # 同上判断tag是否存在
    coreDL(current_page_html)  # 下载第一页
    FLAG = True  # 比较关键的FLAG 不是很喜欢while True 有一个flag比较好控制吧？
    current_page_number = 1  # 同上默认第一页
    while FLAG == True:
        answer = input('是否下载下一页内容：[Y/N]')
        if answer[0] == 'Y' or answer[0] == 'y':
            print(current_page_url)
            (next_page_url, next_page_number) = crawler.next_page(current_page_url, current_page_number)
            print(next_page_url, next_page_number)
            current_page_number = current_page_number + 1
            coreDL(crawler.getSource(next_page_url))
            FLAG = True
        else:  # 这里跳FLAG
            FLAG = False

    return True


def main():
    choice = int(input('请输入选项\n 1 ) 连续多页下载 \n 2 ) 单个页面下载\n'))
    if choice == 1:
        MultiPageDownload()
    else:
        SinglePageDownload()


if __name__ == '__main__':
    main()
