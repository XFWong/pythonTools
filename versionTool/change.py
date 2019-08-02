#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import logging
import sys
import operator as op


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='D:/test.log',
#                     filemode='w')

# logging.disable(logging.CRITICAL)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s:%(message)s')
currpath = os.getcwd()
fileName = os.listdir(currpath)

currpathFile = currpath + '\\' + 'OnlyBin.txt'
logging.debug('filename:%s', currpathFile)
# logging.debug('path exis :%d',os.path.exists(currpath),'file
# exits:%d',os.path.isfile(currpath))
logging.debug('path exis :%s, file exists:%s',
              os.path.exists(currpath), os.path.isfile(currpathFile))
if os.path.isfile(currpathFile):

    file = open(currpathFile, 'r+')
    logging.debug(file)
    content = file.read()
    # file point reset
    file.seek(0)
    # for i in content:
    # logging.debug(content)
    srcVer = input('Please input old so version, like 09 10:')
    # inCmd = '(\'+srcVer
    inCmd = '(%s_){1,}' % srcVer
    logging.debug('inCmd%s' % inCmd)
    regex = re.compile(r'%s' % inCmd)
    se = regex.findall(content)
    if not se:
        logging.error('can not find that version, exit!!!!!')
        sys.exit(-1)
    logging.debug(se)
    logging.debug(len(se))
    desVer = input('Please input new so version, like 09 10:')
    desVerEnd = desVer + '_'
    tihuan = regex.sub(desVerEnd, content)
    logging.debug(tihuan)
    isConfirm = input('please input y to confirm modify, n to cancell modify: ')
    if op.eq(isConfirm.lower(), 'y'):
        file.write(tihuan)
        logging.debug('Modify OK')
    else:
        logging.debug('Cancell!!')
        file.close()
else:
    logging.error('OnlyBIN.txt is not exist')

# file1 = open('test.txt', 'w')
# file1.write('hello file')
# file1.close()
# file1 = open('test.txt', 'r+')
# we=file1.read()
# print(we)
# logging.debug(content)
