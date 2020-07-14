from bs4 import BeautifulSoup
import requests, os, time, re

#initial setup
dir = 'Text/theromantic/'
os.makedirs(dir, exist_ok = True)

#read file for links and clean them up
link_dir = 'Text/links.txt'
with open(link_dir,'r') as f:
    links = f.readlines()

for i,link in enumerate(links):
    link = link.replace('\n','')
    links[i] = link



#extracts the text
def extract_text(soup):
    h3 = soup.findAll('h3')
    h3 = h3[0]
    title = re.sub('<[^>]*>','',str(h3))

    poem = []
    p = h3.find_next_sibling()
    while '<div' not in str(p):
        if '<p>' in str(p):
            poem.append(p)
        p = p.find_next_sibling()

    text = title + '\n'
    for i,item in enumerate(poem):
        item = str(item)
        item = item.replace('<br/>','\n')
        item = item.replace('</p>','\n')
        item = re.sub('<[^>]*>','',item)
        """
        poem = poem.replace('\u2665','')
        poem = poem.replace('\x96','')
        poem = poem.replace('\x91','')
        poem = poem.replace('\n\n','\n')
        poem = poem[1:]
        """
        text += item + '\n'

    """
    poem = str(h1.find_next('td'))

    poem = poem.replace('<br/>','\n')
    poem = re.sub('<[^>]*>','',poem)
    poem = re.sub('-[^-]*-','',poem)
    poem = poem.replace(' '*18,'')
    poem = poem.replace('\u2665','')
    poem = poem.replace('\x96','')
    poem = poem.replace('\x91','')
    poem = poem.replace('\n\n','\n')
    poem = poem[1:]


    h1 = str(h1[0])
    pos = re.search('>.*<',str(h1))
    title = h1[pos.start()+1:pos.end()-1]

    p = soup.findAll('p')
    for i,item in enumerate(p):
        item = str(item)
        if '<p>' in item:
            p[i] = re.sub('<(|.)p>','',item)

    pre = soup.findAll('pre')
    for i,item in enumerate(pre):
        item = str(item)
        pre[i] = re.sub('<(|.)pre>','',item)

    divs = soup.findAll('div',{'class':'poem__body'})
    divs = str([i for i in divs if 'card__body' not in str(i)][0])

    #try to parse the divs into something more readible
    text = divs.replace('<br/>','\n')
    text = re.sub('<[^>]*>','',text)
    text = text.replace('\u2028','')
    """

    return text

#gathering the data
data = []
for i,link in enumerate(links):
    print(i)
    #try:
    res = requests.get(link)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'lxml')

    data.append(extract_text(soup))

    #except:
        #print(f'Error: link {link} not found')

#writing the data to files
for item in data:
    filename = dir + re.sub(r'\W+','',item)[:10] + '.txt'
    with open(filename,'w') as f:
        f.write(item)
