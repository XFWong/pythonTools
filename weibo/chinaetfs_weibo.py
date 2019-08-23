#!/usr/bin/env python3
# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import re
import os
import jieba
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image


s = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
mainUrl = 'https://www.weibo.com/chinaetfs'
login_url = 'https://www.weibo.com/login.php'

ARTILE = 'chinaetfs_weibo.txt'
# 词云形状图片
WC_MASK_IMG = 'shade.jpg'
# WC_MASK_IMG = 'etfs.jpg'
# 词云字体
WC_FONT_PATH = '叶立群几何体.ttf'


def writ_to_file(content):
    with open(ARTILE, 'a+', encoding='utf-8') as file:
        file.write(content)


def spilder_url():
    try:
        print('拉取第1页url')
        print(mainUrl)
        r = s.get(login_url, headers=headers)
        r = s.get(mainUrl, headers=headers)
    except Exception as e:
        print(r.raise_for_status())
    else:
        soup = BeautifulSoup(r.content, 'lxml')
        writ_to_file(soup.prettify())
        return
        # print(soup.prettify())
        # 提取本页的所有URL及其他页面的url
        urlPage = set()
        urlContent = set()
        begin = 0
        end = 0
        for urls in soup.find_all('a'):
            # print(urls['href'])
            if re.match(r'https://www.chinaetfs.net/\?p=\d+', urls['href']):
                urlContent.add(urls['href'])
            if re.match(r'https://www.chinaetfs.net/\?paged=\d+', urls['href']):
                urlPage.add(urls['href'])
                data = int(re.search(r'\d+', urls['href']).group())
                if data > begin:
                    begin = end
                    end = data
                    print('begin:%d, end:%d' % (begin, end))

        for i in range(begin, (end + 1)):
            print('拉取第%d页url' % i)
            urlmother = 'https://www.chinaetfs.net/?paged=%d' % i
            print(urlmother)
            try:
                r = s.get(urlmother, headers=headers)
            except Exception as e:
                print('拉取第%d页url失败!' % i)
                print(r.raise_for_status())
            else:
                soup = BeautifulSoup(r.content, 'lxml')
                for urls in soup.find_all('a'):
                    if re.match(r'https://www.chinaetfs.net/\?p=\d+', urls['href']):
                        urlContent.add(urls['href'])
        # print(urlContent)
        # print(urlPage)
        urlAll = list(urlContent)
        return urlAll
        # print(urlAll)


# 提取数字
def embeded_number(s):
    result = int(re.search(r'\d+', s).group())
    # print(result)
    return result


def spilder_content(urlAll):
    # urlAll = ['https://www.chinaetfs.net/?p=1260']

    title, time, artile = '', '', ''
    if urlAll != None:
        print('共%d篇' % len(urlAll))
        i = 0
        urlAll.sort(key=embeded_number)
        print(urlAll)
        for url in urlAll:
            try:
                i += 1
                print('拉取第%d篇文章' % i)
                print(url)
                r = s.get(url, headers=headers)
            except Exception as e:
                print('%s 失败!' % url)
            else:
                with open(ARTILE, 'a+', encoding=r.encoding) as file:
                    soup = BeautifulSoup(r.content, 'lxml')
                    # print(soup.find_all('header', class_='entry-header'))
                    for child in soup.find_all('header', class_='entry-header'):
                        try:
                            title = child.h1.string
                            time = child.time.string
                        except Exception as e:
                            print('no title!')
                            title = 'No title'
                        else:
                            print(title, time)
                    for child in soup.find_all('div', class_='entry-content'):
                        artile = child.get_text()
                    print(artile)
                    file.write(title)
                    file.write('\t\t\t%s\n' % time)
                    file.write('URL: ' + url)
                    file.write('\n\n')
                    file.write(artile)
                    file.write('\n\n')
        print('拉取所有文章成功！共%d篇' % i)


def cut_word():
    with open(ARTILE, encoding='utf-8') as file:
        artile = file.read()
        wordlist = jieba.cut(artile, cut_all=True)
        wl = ' '.join(wordlist)
        return wl


def create_wordcloud():
    wc_mask = np.array(Image.open(WC_MASK_IMG))
    stop_words = ['URL', 'https', 'www', 'net', 'com', 'xueqiu'
                  'chinaetfs', '什么', '为什么', '这样', '可以', '他们', '那么', '没有', '如果',
                  '只有', '不是', '没有', '或者', '已经', '自己', '我们', '这个', '还是', '真的', '只是',
                  '就是']
    wc = WordCloud(background_color='black', max_words=500, mask=wc_mask, scale=4,
                   max_font_size=70, random_state=42, stopwords=stop_words, font_path=WC_FONT_PATH)
    wc.generate(cut_word())
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    # plt.show()
    wc.to_file('chinaetfs.png')


def main():
    # s = 'https://www.chinaetfs.net/?p=969'
    # embeded_number(s)
    # 文章存在则提取分词并生成词云
    if os.path.exists(ARTILE):
        # print(cut_word())
        create_wordcloud()

    else:
        spilder_url()
        # spilder_content(spilder_url())


if __name__ == '__main__':
    main()
