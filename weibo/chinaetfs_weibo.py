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
# mainUrl = 'https://m.weibo.cn/u/5687069307'
mainUrl = 'https://m.weibo.cn/api/container/getIndex'
headers = {
    'host': 'm.weibo.cn',
    'refer': 'https://m.weibo.cn/u/5687069307',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1',
    'X-Requested-With': 'XMLHttpRequest'
}
params = {
    'type': 'uid',
    'value': '5687069307',
    'containerid': '1076035687069307',
    'page': '{page}'
}
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
    page_total = 100000
    page = 1
    last_length = 0
    with open(ARTILE, 'a+', encoding='utf-8') as file:
        for i in range(page_total):
            content_length = 0
            artile = ''
            try:
                print('拉取第%d页url' % page)
                print(mainUrl)
                # params['page'] = str(page)
                params['page'] = page
            # r = s.get(login_url, headers=headers)
                r = s.get(mainUrl, headers=headers, params=params)
                cards = r.json().get('data').get('cards')
            except Exception as e:
                print(r.raise_for_status())
            else:
                page += 1
                for card in cards:
                    if card.get('card_type') == 9:
                        text = card.get('mblog').get('text')
                        time = card.get('mblog').get('created_at')
                        # print(time)
                        artile += time + '\n'
                        # print(artile)
                        urlPart = re.search(
                            r'(?<=\.\.\.<a href=").+(?=">)', text)
                        if urlPart != None:
                            ulr = 'https://m.weibo.cn' + urlPart.group()
                            print(ulr)
                            r = s.get(ulr, headers=headers)
                            # print(r.text)
                            soup = BeautifulSoup(r.content, 'lxml')
                            for child in soup.find_all('script'):
                                # print(child.get_text())
                                content = re.search(
                                    r'(?<="text": ").+(?=")', child.get_text())
                                if content != None:
                                    artile += (
                                        re.sub(r'[<br/> ]', '', content.group()))
                                    # print(text)
                                    # content.append(artile)
                                    artile += '\n\n'
                                    # print(artile)
                        else:
                            pattern = re.compile(r'<.*?>|转发微博|查看图片')
                            artile += re.sub(pattern, '', text)
                            artile += '\n\n'
                            # print(artile)
                            # content.append(artile)
            content_length = len(artile)
            print('content_length %d' % content_length)
            if content_length == last_length:
                print('没有更多的微博了')
                return
            else:
                print(artile)
                file.write(artile)
                last_length = content_length
                content_length = 0
                print('last_length:%d' % last_length)

    # print(soup.prettify())
    # 提取本页的所有URL及其他页面的url
    # urlPage = set()
    # urlContent = set()
    # begin = 0
    # end = 0
    # for urls in soup.find_all('a'):
    #     # print(urls['href'])
    #     if re.match(r'https://www.chinaetfs.net/\?p=\d+', urls['href']):
    #         urlContent.add(urls['href'])
    #     if re.match(r'https://www.chinaetfs.net/\?paged=\d+', urls['href']):
    #         urlPage.add(urls['href'])
    #         data = int(re.search(r'\d+', urls['href']).group())
    #         if data > begin:
    #             begin = end
    #             end = data
    #             print('begin:%d, end:%d' % (begin, end))

    # for i in range(begin, (end + 1)):
    #     print('拉取第%d页url' % i)
    #     urlmother = 'https://www.chinaetfs.net/?paged=%d' % i
    #     print(urlmother)
    #     try:
    #         r = s.get(urlmother, headers=headers)
    #     except Exception as e:
    #         print('拉取第%d页url失败!' % i)
    #         print(r.raise_for_status())
    #     else:
    #         soup = BeautifulSoup(r.content, 'lxml')
    #         for urls in soup.find_all('a'):
    #             if re.match(r'https://www.chinaetfs.net/\?p=\d+', urls['href']):
    #                 urlContent.add(urls['href'])
    # print(urlContent)
    # print(urlPage)
    # urlAll = list(urlContent)
    # return urlAll
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
