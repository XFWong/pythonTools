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
WC_MASK_IMG = 'shade.jpg'
# WC_MASK_IMG = 'alice_color.png'
# 影评数据保存文件
COMMENTS_FILE_PATH = 'douban_comments.txt'
URL_PATH = 'url.txt'
# 词云字体
WC_FONT_PATH = '叶立群几何体.ttf'

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


def spider_comment():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    urls = []
    with open(URL_PATH, 'r') as file:
        for line in file:
            urls.append(line)
    try:
        i = 0

        for element in urls:
            i += 1
            print('提取第%d个评论' % i)
            url = element.strip('\n')
            print(url)
            r = s.get(url, headers=headers)
            if r.raise_for_status() != None:
                print(r.raise_for_status())
            with open(COMMENTS_FILE_PATH, 'a+', encoding=r.encoding) as file:
                soup = BeautifulSoup(r.content, features='lxml')
                for comment in soup.find_all('div', class_='review-content clearfix'):
                    # 提取100字以上的评论
                    # print(comment.p.string)
                    if comment.get_text() != None and len(comment.get_text()) > 100:
                        title = '\n\n\t\t\t\t############第%d个评论####作者： %s#######\n\n' % (
                            i, comment.attrs['data-author'])
                        file.write(title)
                        file.write(comment.get_text())
                        file.write('\n')
                # break
    except Exception as e:
        print(e.message)
        print('The %d  happens error! ' % i)
    else:
        print('提取评论成功！共%d条' % i)


# 测试使用哦
def extract_content():
    soup = BeautifulSoup(open(COMMENTS_FILE_PATH), features='lxml')
    # print(soup.prettify)
    i = 0
    for comment in soup.find_all('div', class_='review-content clearfix'):
        i += 1
        # print(comment)
        print(comment.get_text())
        # print(comment.attrs)
        # print(comment.attrs['data-author'])
        # for child in comment:
        #     author = child.get('data-author')
        #     print(author)
    print(i)
    # if comment.string != None:
    #     print(comment.string)
    # for comment in soup.find_all('p') or comment in soup.find_all('div'):
    #     if comment.string != None and len(comment.string) > 100:
    #         i += 1
    #         print(i)


def spider_url():
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
    return 1


def cut_word():
    with open(COMMENTS_FILE_PATH, encoding='utf-8') as file:
        comment_text = file.read()
        wordlist = jieba.cut(comment_text, cut_all=True)
        wl = ' '.join(wordlist)
        # print(wl)
        return wl


def create_word_cloud():
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    stop_words = ['是','可以','自己','没有','就是','作者','of','and','一些','一个','一只','一样','一种','一点',
    'the']
    wc = WordCloud(background_color='white', max_words=200, mask=wc_mask, scale=4,
                   max_font_size=50, random_state=42, stopwords=stop_words, font_path=WC_FONT_PATH)
    wc.generate(cut_word())

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    # plt.figure()
    # plt.show()
    wc.to_file('douban.png')


def main():
    # extract_content()

    if os.path.exists(COMMENTS_FILE_PATH):
        create_word_cloud()
    else:
        accout = input('Please input your accout:\n')
        password = getpass.getpass('your password:\n')
        login_douban(accout, password)
        if os.path.exists(URL_PATH):
            spider_comment()
        else:
            spider_url()


if __name__ == '__main__':
    main()
