#!/usr/bin/env python3
# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import re

s = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
mainUrl = 'https://www.chinaetfs.net'
urlAll = []
ARTILE = 'ChinaEtfs.txt'


def spilder_url():
    try:
        print('拉取第1页url')
        print(mainUrl)
        r = s.get(mainUrl, headers=headers)
    except Exception as e:
        print(r.raise_for_status())
    else:
        soup = BeautifulSoup(r.content, 'lxml')
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
        print(urlContent)
        print(urlPage)
        urlAll = list(urlContent)


def spilder_content():
    # urlAll = ['https://www.chinaetfs.net/?p=1260']
    title, time, artile = '', '', ''
    if urlAll != None:
        i = 0
        for url in urlAll:
            try:
                i += 1
                print('拉取第%d篇文章' % i)
                r = s.get(url, headers=headers)
            except Exception as e:
                print('%s 失败!' % url)
            else:
                with open(ARTILE, 'a+', encoding=r.encoding) as file:
                    soup = BeautifulSoup(r.content, 'lxml')
                    # print(soup.find_all('header', class_='entry-header'))
                    for child in soup.find_all('header', class_='entry-header'):
                        title = child.h1.string
                        time = child.time.string
                    print(title, time)
                    for child in soup.find_all('div', class_='entry-content'):
                        artile = child.get_text()
                    print(artile)
                    file.write(title)
                    file.write('\t\t\t%s' % time)
                    file.write('\n\n')
                    file.write(artile)
        print('拉取所有文章成功！共%d篇' % i)


def main():
    spilder_url()
    spilder_content()


if __name__ == '__main__':
    main()
