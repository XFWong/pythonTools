#!/usr/bin/env python3
# -*- coding: utf-8 -*
import os
import re
import time
import random
import requests
import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import getpass
from bs4 import BeautifulSoup

# 词云形状图片
WC_MASK_IMG = 'Emile.jpg'
# 影评数据保存文件
COMMENTS_FILE_PATH = 'douban_comments.txt'
URL_PATH = 'url.txt'
# 词云字体
WC_FONT_PATH = '/Library/Fonts/Songti.ttc'

s = requests.Session()


def login_douban(accout, password):
    login_url = 'https://accounts.douban.com/j/mobile/login/basic'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
               'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony'}
    data = {'name': 'account',
            'password': 'password',
            'remember': 'false'}
    data['name'] = accout
    data['password'] = password
    # print(data)

    try:
        r = s.post(login_url, headers=headers, data=data)
        r.raise_for_status()
    except:
        print('login fail!')
        return 0
    print(r.text)
    return 1


def spider_comment(page=0):
    """
    爬取某页影评
    :param page: 分页参数
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    bookreview = 'https://book.douban.com/subject/10606457/reviews'
    try:
        print('开始爬取第1页url')
        r = s.get(bookreview, headers=headers)
        r.raise_for_status()
    except:
        print('get comment_url fail')
    soup = BeautifulSoup(r.content, features='lxml')
    urls = soup.find_all('a', href=re.compile(
        r'https://book.douban.com/review/\d+/'))
    # print(r.text)
    # print(urls)
    with open(URL_PATH, 'a+') as file:
        for link in urls:
            if not re.search(r'\#', link.get('href')):
                file.write(link.get('href'))
                file.write('\n')

    # 爬取后面页
    totalPageSoup = soup.find_all(
        'span', attrs={'data-total-page': re.compile(r'\d')})
    totalPage = 0
    for total in totalPageSoup:
        totalPage = int(total.get('data-total-page'))
    print('共%d页url, 还剩%d页' % (totalPage, totalPage - 1))
    for i in range(1, totalPage):
        print('开始爬取第%d页url' % (i + 1))
        page = int(i * 20)
        pageUrl = 'https://book.douban.com/subject/10606457/reviews?start=%d' % page
        try:
            r = s.get(pageUrl, headers=headers)
            r.raise_for_status()
        except:
            print('get comment_url fail:%d' % page)
        soup = BeautifulSoup(r.content, features='lxml')
        urls = soup.find_all('a', href=re.compile(
            r'https://book.douban.com/review/\d+/'))
        # print(r.text)
        # print(urls)
        with open(URL_PATH, 'a+') as file:
            for link in urls:
                if not re.search(r'\#', link.get('href')):
                    file.write(link.get('href'))
                    file.write('\n')
    print('URL提取完成！！')
    # print('开始爬取第%d页' % int(page))
    # start = int(page * 20)
    # comment_url = 'https://movie.douban.com/subject/1905462/comments?start=%d&limit=20&sort=new_score&status=P' % start
    # # 请求头

    # try:
    #     r = s.get(comment_url, headers=headers)
    #     r.raise_for_status()
    # except:
    #     print('第%d页爬取请求失败' % page)
    #     return 0
    # # 使用正则提取影评内容
    # comments = re.findall('<span class="short">(.*)</span>', r.text)
    # if not comments:
    #     return 0
    # # 写入文件
    # with open(COMMENTS_FILE_PATH, 'a+', encoding=r.encoding) as file:
    #     file.writelines('\n'.join(comments))
    return 1


def main():
    if not os.path.isfile(URL_PATH):
        with open(URL_PATH, 'r') as file:
            content = file.read()
            print(content)
    else:
        accout = input('Please input your accout:\n')
        password = getpass.getpass('your password:\n')
        if login_douban(accout, password):
            spider_comment(1)


if __name__ == '__main__':
    main()
