from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pprint
from urllib.parse import urlparse
import queue
import validator_collection

print("Please enter the URL: ")
weblink = input()
unvisitedlinks = queue.Queue()
unvisitedlinks.put(weblink)
visitedlinks = []
#txtfile= open("links.txt", "w")

def fetchpage(url):
    parsed_uri = urlparse(url)
    baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    try:
        req = Request(url)
        html_page = urlopen(req)
    except:
        print('Error opening the URL')
    soup = BeautifulSoup(html_page, "lxml")
    text = soup.get_text()
    print(text)
    for link in soup.findAll('a'):
        url = str(link.get('href'))
        print('The link is', url)
        if url.startswith('http') and url not in visitedlinks:
            unvisitedlinks.put(url)
            #txtfile.write("%s\n" % url)
        elif url.startswith('/'):
            url = baseurl + url
            if url not in visitedlinks:
                unvisitedlinks.put(url)
                #txtfile.write("%s\n" % url)

while not unvisitedlinks.empty():
    url = unvisitedlinks.get()
    if validator_collection.is_url(url) and url not in visitedlinks:
        try:
            print('Trying to connect to page')
            fetchpage(url)
            visitedlinks.append(url)
        except:
            print('Error visiting URL')
    else:
        print('Invalid URL!')
    print('UNVISITED LINKS = ' + str(unvisitedlinks.qsize()))
    print('VISITED: ' + str(len(visitedlinks)))
    
#txtfile.close()
