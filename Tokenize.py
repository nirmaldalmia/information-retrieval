from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pprint
from urllib.parse import urlparse
import queue
import validator_collection
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
nltk.download('punkt')
nltk.download('stopwords')

print("Please enter the URL: ")
weblink = input()
unvisitedlinks = queue.Queue()
unvisitedlinks.put(weblink)
visitedlinks = []
stop_words = set(stopwords.words('english'))
stop_words = stop_words.union(",","(",")","[","]","{","}","#","@","!",":",".", ";")
ss=SnowballStemmer('english')
txtfile= open("tokens.txt", "w")

def tokenizer(soup):
    for paragraph in soup.findAll('p'):
        sentence = paragraph.text
        words = word_tokenize(sentence)
        for w in words:
            token = ss.stem(w)
            if token not in stop_words:
                txtfile.write("%s\n" % token)
                print(token)

def fetchpage(url):
    parsed_uri = urlparse(url)
    baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    try:
        req = Request(url)
        html_page = urlopen(req)
    except:
        print('Error opening the URL')
    soup = BeautifulSoup(html_page, "lxml")
    tokenizer(soup)
    #text = soup.get_text()
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
    
txtfile.close()
