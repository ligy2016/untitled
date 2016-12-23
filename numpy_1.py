#coding=utf-8
# import numpy as np
# from pandas import  *
import sys
# import pandas as pd
from  datetime  import  *
import  time
import linecache
def analysis_data(path,eth,start,end):
    # fo = open("d:/foo.txt", "wb")
    # fo.write("www.runoob.com!\nVery good site!\n");
    # fo.close()
    # data = pd.read_table('d:/ljt.log',encoding='utf-8',sep='\s+')
    lines = linecache.getlines(path)
    i = 0
    startindex = 0
    endindex = 0
    for line in lines:

        if str(line).strip() == start:
            startindex= i
        if str(line).strip() == end:
            endindex = i
            break
        i +=1
    print startindex,endindex
    line_s = lines[startindex+3+int(eth)].strip().split()
    line_e =lines[endindex+3+int(eth)].strip().split()
    # p = ','.join(s.split())
    # print s.replace('_','-')
    # print line_s,line_e
    liuliang_receive = int(line_e[1]) - int(line_s[1])
    packet_receive =   int(line_e[2]) - int(line_s[2])
    liuliang_transmit = int(line_e[9]) - int(line_s[9])
    packet_transmit = int(line_e[10]) - int(line_s[10])
    start_datetime = datetime.strptime(start, "%Y_%m_%d %H:%M:%S")
    end_datetime = datetime.strptime(end, "%Y_%m_%d %H:%M:%S")
    print 'eth%s,起始时间：%s，结束时间：%s, 接收流量：%d, 接收包：%d,发送流量：%d ,发送包：%d,耗时：%d秒' %\
          (eth,start,  end, liuliang_receive,packet_receive,liuliang_transmit,packet_transmit,(end_datetime-start_datetime).seconds)

def test_pandas():
    obj = pandas.Series([4,7,-5,3])
    print obj

# arry1 = np.array(data1)
# print arry1,arry1.dtype

if __name__ == '__main__':
    # print sys.argv[1]
    analysis_data(path = sys.argv[1],eth = sys.argv[2],start=sys.argv[3],end = sys.argv[4])
