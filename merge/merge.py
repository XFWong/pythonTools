#!/usr/bin/env python3
# -*- coding: utf-8 -*

import re

BLOG_FILE = 'ChinaEtfs.txt'
WEIBO_FILE = 'chinaetfs_weibo.txt'
ALL_FILE = 'all_file.txt'


def update_weibo_time():
    with open(WEIBO_FILE, 'r+', encoding='utf-8') as weibo:
        weibo_content = weibo.read()
        weibo.seek(0)
        weibo_content_new = ''
        for content in re.split(r'#########', weibo_content):
            # print(content)
            search_pattern = re.compile(r'^\d{1,2}-\d{1,2}', re.M)
            time_result = re.search(search_pattern, content)
            if time_result != None:
                weibo_time = '2019-' + time_result.group()
                # print(weibo_time)
                weibo_content_new += re.sub(search_pattern,
                                            weibo_time, content)
            else:
                weibo_content_new += content
            weibo_content_new += '#########'
        # print(weibo_content_new)
        weibo.write(weibo_content_new)


def merge_file(file1=BLOG_FILE, file2=WEIBO_FILE, file3=ALL_FILE):
    # 合并后的文章需要按照时间升序排列
    with open(file1, encoding='utf-8') as blog, open(file2, encoding='utf-8') as weibo, open(file3, 'a+', encoding='utf-8') as merge:
        # pattern = re.compile(r'\d{4}年\d{1,2}月\d{1,2}')
        # blog_date_all = pattern.findall(blog_content)
        # print(blog_date_all)
        # for line in blog.readlines():
        #     print(line)
        # blog_lines = blog.readlines()
        # weibo_lines = weibo.readlines()
        # one_blog = ''
        # for blog_line in blog_lines:
        #     result = re.search(pattern, blog_line)
        #     if result != None:
        #         print(result.group())
        #         one_blog += result.group()
        #     else:
        #         one_blog += blog_line
        #         print(one_blog)

        # for weibo_line in weibo_lines:
        #     print(blog_line)
        blog_content = blog.read()
        weibo_content = weibo.read()
        merge_content = ''
        pattern = re.compile(r'#########')
        for blog_content_oneday in re.split(pattern, blog_content):
            patern_time = re.compile(r'\d{4}年\d{1,2}月\d{1,2}')
            blog_time_result = re.search(patern_time, blog_content_oneday)
            if blog_time_result != None:
                blog_time = re.sub(r'\D', '-', blog_time_result.group())
                # print(time)
                for weibo_content_oneday in re.split(pattern, weibo_content):
                    # print(content)
                    patern_time = re.compile(r'\d{4}-\d{1,2}-\d{1,2}', re.M)
                    weibo_time_result = re.search(
                        patern_time, weibo_content_oneday)
                    if weibo_time_result != None:
                        weibo_time = re.sub(
                            r'(?<=-)0', '', weibo_time_result.group())
                        if weibo_time <= blog_time:
                            print(weibo_time, blog_time)
                            merge_content += weibo_content_oneday
                            # print(merge_content)
            merge_content += blog_content_oneday
        print(merge_content)
        # merge.write(merge_content)
        # print(weibo_time)
        # weibo_content_tmp = re.sub(
        #     patern_time, weibo_time, weibo_content_tmp)
        # print(weibo_content_tmp)


if __name__ == '__main__':
    merge_file()
    # update_weibo_time()
