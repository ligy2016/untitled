
class FindNews(object):
    def __init__(self):
        self.last_url_set = set()
        self.this_url_set= set()
        self.new_url_set= set()
        self.content_dic= {}
    def AddUrl(self,url,title):
        self.this_url_set.add(url)
        # self.content_dic.
        if url not in last_url_set:
            return True
            #insert into db

    def UpdateSet(self):
        last_url_set = self.this_url_set
        self.this_url_set.clear()

class c1(object):
    def fun1(self):
        print "i am c1.fun1"

class c2(object):
        def fun2(self):
            c1.fun1()


if __name__ == '__main__':
    c =c2()
    c.fun2()


last_url_set = set('spam')
x.add('lgy')
x.add('www.163.com')

y=set(x)
y.add('wwwwww')

print x
print y-x

