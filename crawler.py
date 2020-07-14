from bs4 import BeautifulSoup
import requests, os, time, re

#setup directory
initial_page = 'https://theromantic.com/love_poems/main.htm'
dir = 'Text/'
os.makedirs('Text',exist_ok=True)

#filter site for all links
def link_getter():
    links = []
    for a in soup.find_all('a', href=True):
        links.append(a['href'])
    return(links)

#checks if item is valid
def valid(item):
    if 'http://theromantic.com/love_poems/' in str(item):
        return True
    else:
        return False

#gather website html
res = requests.get(initial_page)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

#find all links and filter out desired ones
linkElem = link_getter()
filtered = filter(valid,linkElem)

#dump links in a file
with open(dir+'links.txt','w') as f:
    for addr in filtered:
        f.write(addr+'\n')
