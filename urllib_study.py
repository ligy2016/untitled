
# -*- coding:GBK -*-
# !/usr/bin/python

import urllib2

def test():
    write_file_new()
def test1():
    c = '��'
    s= '�л����񹲺͹�ABC'
    print is_chinese(c)
def write_file_new():
    f_new = file('d:/ws.txt', 'w+')
    f = urllib2.urlopen('http://wallstreetcn.com/node/258102')
    lines = f.readlines()

    # f_new.write(line)
    f_new.writelines(lines)
def is_chinese(uchar):

        """�ж�һ��unicode�Ƿ��Ǻ���"""

        if uchar >= u'/u4e00' and uchar<=u'/u9fa5':

                return True

        else:

                return False
if __name__ == '__main__':
    test1()
