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
from anytree import Node, RenderTree
nltk.download('punkt')
nltk.download('stopwords')

print("Please enter the URL: ")
weblink = input()
print("Please enter the keywords: ")
keywords = input()
seed = Node(weblink)
unvisitedlinks = queue.Queue()
unvisitedlinks.put(weblink)
visitedlinks = []
stop_words = set(stopwords.words('english'))
stop_words = stop_words.union(",","(",")","[","]","{","}","#","@","!",":",".", ";")
ss=SnowballStemmer('english')
txtfile= open("dict.txt", "w")
dictionary = {}

def InvertedIndex(token, url):
    if token not in dictionary:
        dictionary[token] = [url]
    elif token in dictionary:
        if url not in dictionary[token]:
            dictionary[token].append(url)
    txtfile.write("%s\n" % dictionary)

def tokenizer(soup, url):
    for paragraph in soup.findAll('p'):
        sentence = paragraph.text
        words = word_tokenize(sentence)
        for w in words:
            token = ss.stem(w)
            if token not in stop_words:
                #txtfile.write("%s\n" % token)
                InvertedIndex(token, url)

def fetchpage(url):
    parsed_uri = urlparse(url)
    baseurl = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    try:
        req = Request(url)
        html_page = urlopen(req)
    except:
        print('Error opening the URL')
    soup = BeautifulSoup(html_page, "lxml")
    if keywords in str(soup):
        tokenizer(soup, url)
        #text = soup.get_text()
        for link in soup.findAll('a'):
            url = str(link.get('href'))
            print('The link is', url)
            if url.startswith('http') and url not in visitedlinks:
                unvisitedlinks.put(url)
            elif url.startswith('/'):
                url = baseurl + url
                if url not in visitedlinks:
                    unvisitedlinks.put(url)

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
