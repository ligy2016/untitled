#coding=utf-8
# import numpy as np
# from pandas import  *
import os
import pandas as pd
from  datetime  import  *
import  time
import linecache
def read_data(eth,start,end):
    # data = pd.read_table('d:/ljt.log',encoding='utf-8',sep='\s+')
    lines = linecache.getlines('d:/ljt.log')
    i = 0
    for line in lines:

        if str(line).strip() == start:
            print 'zhaodo start'
            satrtindex= i
        if str(line).strip() == end:
            print 'zhaodo end'
            endindex = i
            break
        i +=1

    line_s = lines[satrtindex+3+eth].strip().split()
    line_e =lines[endindex+3+eth].strip().split()
    # p = ','.join(s.split())
    # print s.replace('_','-')
    # print line_s,line_e
    liuliang = int(line_e[1]) - int(line_s[1])
    start_datetime = datetime.strptime(start, "%Y_%m_%d %H:%M:%S")
    end_datetime = datetime.strptime(end, "%Y_%m_%d %H:%M:%S")
    print 'eth%d,起始时间：%s，结束时间：%s, 流量：%d,耗时：%d秒' %(eth,start,  end, liuliang,(end_datetime-start_datetime).seconds)

def test_pandas():
    obj = pandas.Series([4,7,-5,3])
    print obj

# arry1 = np.array(data1)
# print arry1,arry1.dtype

if __name__ == '__main__':
    read_data(eth = 0,start='2016_12_12 13:42:02',end = '2016_12_12 14:42:02')
