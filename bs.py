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
<p class="story">...</p>"""
# soup = BeautifulSoup(open('www.163.com'))
soup = BeautifulSoup(html,"lxml")
# print soup.prettify()
# print soup.p.attrs
#
# print soup.a.string

# for string in soup.stripped_strings :
#     print(repr(string))
# print soup.find_all('a')
print soup.find_all(href=re.compile("elsie"))