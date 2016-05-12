
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


last_url_set = set('spam')
x.add('lgy')
x.add('www.163.com')

y=set(x)
y.add('wwwwww')

print x
print y-x

