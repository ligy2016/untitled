#coding=utf-8
import httplib, urllib,urllib2
import cookielib
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
# def auto_write_log():
#     # 定义需要进行发送的数据
#     params = urllib.urlencode({'cat_id': '6',
#                                'news_title': '标题-Test39875',
#                                'news_author': 'Mobedu',
#                                'news_ahome': '来源',
#                                'tjuser': 'carchanging',
#                                'news_keyword': '|',
#                                'news_content': '测试-Content',
#                                'action': 'newnew',
#                                'MM_insert': 'true'});
#     # 定义一些文件头
#     headers = {"Content-Type": "application/x-www-form-urlencoded",
#                "Connection": "Keep-Alive", "Referer": "http://192.168.1.212/newsadd.asp?action=newnew"};
#     # 与网站构建一个连接
#     conn = httplib.HTTPConnection("192.168.1.91");
#     # 开始进行数据提交   同时也可以使用get进行
#     conn.request(method="POST", url="/zentao/task-view-1937.html", body=params, headers=headers);
#     # 返回处理后的数据
#     response = conn.getresponse();
#     # 判断是否提交成功
#     if response.status == 302:
#         print "发布成功!^_^!";
#     else:
#         print "发布失败\^0^/";
#     # 关闭连接
#     conn.close();

def log():
    logs = {'body': 'log test'}
    # 模拟登录
    cj = cookielib.CookieJar()
    # 用户名和密码
    post_data = urllib.urlencode({'username': 'ligy', 'password': '888888'})
    # 登录路径
    path = 'http://192.168.1.91/zentao/user-login-L3plbnRhby90YXNrLXZpZXctMTkzNy5odG1s.html'
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Opera/9.23')]
    urllib2.install_opener(opener)
    req = urllib2.Request(path, post_data)
    conn = urllib2.urlopen(req)

    # 比较表单发布博客
    req2 = urllib2.Request('http://192.168.1.91/zentao/task-view-1937.html', urllib.urlencode(logs))
    # 查看表单提交后返回内容
    print urllib2.urlopen(req2).read()
def logs():
    # logs = {'comment': '日志'}
    # para = {'username': 'ligy', 'password': '888888'}
    # r = requests.post('http://192.168.1.91/zentao/user-login.html',para)
    # print r

    driver = webdriver.PhantomJS(executable_path='d:\phantomjs-2.1.1-windows\gbin\phantomjs.exe')
    # driver.get("http://pythonscraping.com/page/javascript/ajaxDemo.html")
    driver.get('http://192.168.1.91/zentao/user-login.html')

    element = driver.find_element_by_id('account')
    element.send_keys("ligy")
    element = driver.find_element_by_name('password')
    element.send_keys("888888")
    driver.find_element_by_id('submit').click()
    time.sleep(1)
    # .cookies.get_dict()
    # r = requests.get
    # req2 = urllib2.Request('http://192.168.1.91/zentao/task-view-1937.html', urllib.urlencode(logs))
    # print urllib2.urlopen(req2).read()
    # r = requests.post('http://192.168.1.91/zentao/task-view-1937.html', logs)
    # print r


    # driver = webdriver.PhantomJS(executable_path='d:\phantomjs-2.1.1-windows\gbin\phantomjs.exe')

    driver.get('http://192.168.1.91/zentao/task-view-1937.html')
    driver.maximize_window()
    driver.find_element(By.LINK_TEXT,'请写日志').click()
    time.sleep(4)
    # print driver.page_source

    # iframe = driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@class,'ke-edit-iframe')]"))
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="commentBox"]/form/div/div/div[2]/iframe'))
    # ele = driver.find_element_by_xpath("//*[@id='commentBox']/form/div/div/div[2]/iframe")
    # print driver.page_source
    # driver.find_element_by_tag_name('body').send_keys('Hello world!')
    driver.find_element_by_class_name('article-content').clear()
    driver.find_element_by_class_name('article-content').send_keys("pppppppppppppp")
    # driver.find_element_by_class_name('article-content').send_keys(Keys.ENTER)
    # driver.find_element_by_class_name('article-content').submit()

    time.sleep(2)

    # print driver.find_element_by_class_name('article-content').text
    print driver.page_source
    # driver.find_element(By.LINK_TEXT,'请写日志').click()
    # element = driver.find_element_by_tag_name('legend')
    # iframe = driver.find_element_by_xpath("//iframe[contains(@class,'ke-edit-iframe')]")

    # driver.switch_to.frame(driver.find_element(By.XPATH,"//iframe[@_class=‘ke-edit-iframe']"))
    # driver.switch_to.frame('iframe')
    # driver.switch_to.frame(2)
    # print 'iframe:',driver.page_source
    # print '1:',driver.find_element_by_tag_name('body').text
    # driver.find_element_by_tag_name('body').send_keys('Hello world!')
    # time.sleep(2)
    # actions = ActionChains(driver)
    # actions.send_keys('Hello world!').send_keys(Keys.RETURN)
    # actions.perform()

    # driver.find_element_by_tag_name('body').send_keys("log!!")
    # print '2:',driver.find_element_by_tag_name('body').text
    # element = driver.find_element_by_id('commentBox')
    # element.send_keys("my log")

    driver.switch_to.default_content()
    # print "default:", driver.page_source
    element = driver.find_element(By.XPATH,'//*[@id="commentBox"]/form/button')
    element.click()
    # print element.text
    # element.click()


    driver.quit()

def main():
    logs()

if __name__ == '__main__':
    main()