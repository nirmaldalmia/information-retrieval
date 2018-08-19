from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pprint

req = Request("http://slashdot.org")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
data=''
for link in soup.findAll('a'):
    url = str(link.get('href'))
    print('The link is', url)
    if url.startswith('http'):
        links.append(url)

print(links)