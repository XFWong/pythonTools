#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import baostock as bs
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s:%(message)s')

lg = bs.login()
# 显示登陆返回信息
logging.debug('login respond error_code:' + lg.error_code)
logging.debug('login respond  error_msg:' + lg.error_msg)

#### 获取历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节
rs = bs.query_history_k_data_plus("sh.600000",
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                  start_date='2017-06-01', end_date='2017-12-31',
                                  frequency="d", adjustflag="3")  # frequency="d"取日k线，adjustflag="3"默认不复权
logging.debug('query_history_k_data_plus respond error_code:' + rs.error_code)
logging.debug('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)
#### 结果集输出到csv文件 ####
result.to_csv("D:/history_k_data.csv", encoding="gbk", index=False)
logging.debug(result)

#### 登出系统 ####
bs.logout()
