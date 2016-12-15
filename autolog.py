#coding=utf-8
import httplib, urllib,urllib2
import cookielib
import requests
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
    logs = {'comment': '日志'}
    para = {'username': 'ligy', 'password': '888888'}
    r = requests.post('http://192.168.1.91/zentao/user-login-L3plbnRhby90YXNrLXZpZXctMTkzNy5odG1s.html',para)
    print r
        # .cookies.get_dict()
    # r = requests.get
    # req2 = urllib2.Request('http://192.168.1.91/zentao/task-view-1937.html', urllib.urlencode(logs))
    # print urllib2.urlopen(req2).read()
    r = requests.post('http://192.168.1.91/zentao/task-view-1937.html', logs)
    # print r

def main():
    logs()

if __name__ == '__main__':
    main()