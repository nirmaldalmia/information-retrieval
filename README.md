# Information Retrieval
This repository contains the list of programs written as a part of the Information Retrieval course. It has all the programs step by step starting from the very basic. To know what a particular program does please refer the table below.

### Index
File Name | Description
--- | ---
WebLinks.py | Basic program to connect to a webpage, fetch all the links associated with it and print it in the console.
LinksCrawler.py | Fetches the links on a page, adds them to a queue, visits them one by one and adds to a visited list. This process is looped until the queue is empty
LinksAndTextCrawler.py | Added functionality to fetch and print the text on the webpage
Tokenize.py | Added tokenization of text on the webpage. Currently, limited to the text in 'p' tags only
InvertedIndex.py | A dictionary based inverted index to store the tokens and their corresponding links. Writes the dictionary to a JSON file 'invindex.json'
Search.py | Uses the InvertedIndex created by the previous script, takes search query and returns the links that contain all the keywords from query
FocusedCrawler.py | Along with the seed URL it also takes keywords. Crawling is done and the page is indexed only if the page contains those keywords exactly.
