import json
from nltk.stem import SnowballStemmer

ss = SnowballStemmer('english')
print('Loading Dictionary ......')
with open('invindex.json', 'r') as fh:
    dictionary = json.load(fh)

query = input('Enter the query: ')
tokens  = query.split()
links=[]
try:
    for keyword in tokens:
        key = ss.stem(keyword)
        links.append(dictionary[key])
    result=set(links[0]).intersection(*links[1:])
    print('The search results are: ')
    print(result)

except:
    print('No matching search results')
   
