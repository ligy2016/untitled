from bs4 import BeautifulSoup
import re
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!--  Elsie  --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
<a href="http://example.net/elsie" class="sister" id="link1"><!--  Elsie  --></a>"""

# soup = BeautifulSoup(open('www.163.com'))
soup = BeautifulSoup(html,"lxml")
# print soup.prettify()
# print soup.p.attrs
#
# print soup.a.string
# print soup.find(attrs={href=True,algin=None})
# print soup.find(True)
# test github

# for string in soup.stripped_strings :
#     print(repr(string))
# print soup.find_all('a')
urldict = {}
def addUrl(urldict, url, title):
    urldict.setdefault(url, []).append(title)
a_set = set()
url_set = set()
a_set = soup.find_all(href=re.compile("com"))
for a in a_set:
    # print a.string.strip(),a["href"]
    url_set.add(a["href"])
# soup.find_all(attrs={"id" = True, "algin" = None})
new_a_set= set()
new_url_set = set()
# print type(new_url_set)
new_a_set = soup.find_all(href=re.compile("."))

for a in new_a_set:
    # print a.string.strip(),a["href"]
    new_url_set.add(a["href"])
    addUrl (urldict,a["href"],a.string.strip())

new_urls = new_url_set.difference(url_set)

for new_url in new_urls:
    print new_url, urldict[new_url]



