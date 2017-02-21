#-*- coding: utf-8 -*-
import sys
import AllNewsLinks
from time import sleep, ctime
while(0):
    print 'loop 1 done at:', ctime()
    sleep(5)
dict2 = {'www.163.com': '网易', 'www.sohu.com': '搜狐'}
for key in dict2.keys():
    print 'key=%s, value=%s' % (key, dict2[key])

# z='中文测试'
# print z