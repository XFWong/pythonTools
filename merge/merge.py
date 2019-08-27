#!/usr/bin/env python3
# -*- coding: utf-8 -*

import re
import datetime

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


def sort_blog_file():
    with open(BLOG_FILE, 'r+', encoding='utf-8') as blog:
        blog_content = blog.read()
        sort_content = {}
        pattern = re.compile(r'#########')
        for blog_content_oneday in re.split(pattern, blog_content):
            # print(blog_content_oneday)
            pattern_time = re.compile(r'\d{4}年\d{1,2}月\d{1,2}')
            blog_time_result = re.search(pattern_time, blog_content_oneday)
            # print(blog_time_result)
            # print(blog_content_oneday)
            if blog_time_result != None:
                exist = 0
                content = []
                for key in sort_content.keys():
                    if key == blog_time_result.group():
                        # for vars in sort_content[key]:
                        #     content.append(vars)
                        if type(sort_content[key]) == list:
                            sort_content[key].append(blog_content_oneday)
                        else:
                            content.append(sort_content[key])
                            content.append(blog_content_oneday)
                            sort_content[key] = content
                        exist = 1
                        # print('111')
                        # print(sort_content)
                        # print(sort_content)
                if exist == 0:
                    sort_content[
                        blog_time_result.group()] = blog_content_oneday
                    # print('000')
                    # print(sort_content)
                else:
                    exist = 0
        # print(sort_content)
        # print(sort_content)

        content_tmp = sorted(
            sort_content.keys(), key=lambda x: datetime.datetime.strptime(x, '%Y年%m月%d'))
        text = ''
        for con in content_tmp:
            if type(sort_content[con]) == list:
                # print(sort_content[con])
                for ele in sort_content[con]:
                    # pass
                    # print(ele)
                    text += ele
                    text += '\n#########\n'
            else:
                text += sort_content[con]
                text += '\n#########\n'
        blog.seek(0)
        blog.write(text)
        # print(text)


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
        pattern = re.compile(r'#########')
        progress = 0
        blog_content_list = re.split(pattern, blog_content)
        # 博客内容已排好序，所以将微博内容插入博客
        for weibo_content_oneday in re.split(pattern, weibo_content):
            # 提取微博时间并查找位置插入博客
            total = len(re.split(pattern, weibo_content))
            progress += 1
            merge_content = ''
            pattern_time = re.compile(r'\d{4}-\d{1,2}-\d{1,2}', re.M)
            weibo_time_result = re.search(pattern_time, weibo_content_oneday)
            if weibo_time_result != None:
                weibo_time = re.sub(
                    r'(?<=-)0', '', weibo_time_result.group())  # 去掉微博时间里面的0
                # 遍历博客时间，寻找位置插入微博内容
                insert = 0
                # print('len:%d' % len(blog_content_list))
                # print(blog_content_list)
                i = 0
                while i < len(blog_content_list):
                    blog_content_oneday = blog_content_list[i]

                    pattern_time = re.compile(
                        r'\d{4}年\d{1,2}月\d{1,2}|\d{4}-\d{1,2}-\d{1,2}')
                    blog_time_result = re.search(
                        pattern_time, blog_content_oneday)
                    # 格式化博客时间为xxxx-xx-xx

                    # print(weibo_content_oneday)
                    if blog_time_result != None:
                        # print(blog_time_result.group())
                        blog_time = re.sub(
                            r'\D', '-', blog_time_result.group())
                        # print(blog_time)
                        if datetime.datetime.strptime(weibo_time, '%Y-%m-%d') <= datetime.datetime.strptime(blog_time, '%Y-%m-%d') and insert == 0:
                            # merge_content += weibo_content_oneday
                            # merge_content += '\n#########\n'
                            # merge_content += blog_content_oneday
                            # merge_content += '\n#########\n'
                            blog_content_list.insert(i, weibo_content_oneday)
                            insert = 1
                            # print('if')
                            # print(merge_content, i)
                        # else:
                        #     blog_content_list.insert(i, weibo_content_oneday)
                            # merge_content += blog_content_oneday
                            # merge_content += '\n#########\n'
                            # print('else')
                            # print(merge_content, i)
                    i += 1
                # print(weibo_content_oneday)
                # print('out blog_content_list')
                # print(merge_content)
                # print('ddddddddd')
                if insert == 0:
                    blog_content_list.insert(
                        len(blog_content_list), weibo_content_oneday)
                # print(blog_content_list)
                # merge_content += weibo_content_oneday
                # merge_content += '\n#########\n'
                # print(merge_content)
                # print('out while!!!')
                # blog_content = merge_content
                # print(blog_content)
                # print('insert:%d' % insert)
            # print(total)
            print('进度: {0} %,共 {1}'.format(
                round(progress * 100 / total), total), end='\r')
            # print(blog_content_list)
        for content_merge in blog_content_list:
            merge.write(content_merge)
            merge.write('\n#########\n')
        # print(weibo_time)
        # weibo_content_tmp = re.sub(
        #     patern_time, weibo_time, weibo_content_tmp)
        # print(weibo_content_tmp)


if __name__ == '__main__':
    merge_file()
    # update_weibo_time()
    # sort_blog_file()
