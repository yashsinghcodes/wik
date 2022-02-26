#!/usr/bin/env python3
import requests
import sys
import os
from bs4 import BeautifulSoup
import random
from requests.api import get

try:
    width,height = os.get_terminal_size()
    p = True
except OSError:
    width = 120
    height = 80
    p = False

# Some ANSI escape color codes
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

colors = ['\033[92m','\033[95m','\033[96m','\033[94m','\033[36m']

# Maybe Future Use
## def get_tags(d, params):
##   if any((lambda x:b in x if a == 'class' else b == x)(d.attrs.get(a, [])) for a, b in params.get(d.name, {}).items()):
##      yield d
##   for i in filter(lambda x:x != '\n' and not isinstance(x, bs4.element.NavigableString) , d.contents):
##    yield from get_tags(i, params)

# Makes request to wikipedia for the code
def req(term):
    global wikiurl 
    wikiurl = "https://en.wikipedia.org/wiki/"+term
    r = requests.get(wikiurl)
    return r.text

# Gets summary
def getSummary(term):
    final_content = []
    content = req(term)
    soup = BeautifulSoup(content,'html.parser')
    content = soup.find_all('p')
    # prints the title in the center
    print('\n'+(color.BOLD+str(term)).center(width,"-")+ "\n"+color.END) 
    for i in content:
        # Removing all empty lines
        if i.get_text() == "\n": continue
        else:
            # Removing all external links from the article
            if i('sup'):
                for tag in i('sup'): tag.decompose() 
            
            data = i.get_text()
            final_content.append(data)
            if len(final_content) == 3: break # Breaks after 3 line of content
    
    # Search for other if not available
    if "may refer to:" in str(i):
        print("Did You Mean: ")
        term = searchInfo(term)
    else:
        print(colors[random.randrange(len(colors)-1)]) 
        print(*final_content,sep = '\n\n')
        print(color.END)


def getInfo(term):
    final_content = []
    content = req(term)
    soup = BeautifulSoup(content,'html.parser')
    content = []
    # Seprating Titles from the paragraphs
    for a in soup.find_all(['p','span']):
        try:
            if a['class'] and 'mw-headline' in a['class']:
                content.append(a)
        except KeyError:
            if a.name == 'p':
                content.append(a)

    ## content = soup.find_all(['p',['span', {'class':'mw-headline'}]])
    ## content = soup.find_all(re.compile('p|span'), {'class':re.compile('|mw-headline')})#['p',('span' , {"class": "toctext"})]) 
    ## content = list(get_tags(soup),{'p':{}, 'span':{'class': 'mw-headline'}})

    # Remove all external links
    for i in content:
        if i('sup'):
            for tag in i('sup'): tag.decompose()

        # Getting data    
        data = i.get_text()
        if i.name == 'span': 
            final_content.append('!'+str(data)) # Seprating titles
        else: final_content.append(data)

    # Search if not found
    if "may refer to:" in str(final_content[0]): term = searchInfo(term)

    # Printing the output
    else:
        if p == True: 
            print('\n'+(color.BOLD+str(term)).center(width,"-")+color.END+'\n')
            print(color.BLUE+str(wikiurl).center(width," ")+color.END+'\n')
        else:
            print('\n'+str(term).center(width,"-"))
            print('\n'+str(wikiurl).center(width, " ")+'\n')
        for i in final_content:
            if i == "\n": continue
            if i in ["!See also","!Notes","!References","!External links","!Further reading"]: continue
            else:
                if p == True:
                    if str(i[0]) == '!':
                         print(color.BOLD+colors[random.randrange(len(colors)-1)]+i[1:]+color.END+color.END)
                         print("-"*(len(i)+1))
                    else:   
                        if "Other reasons this message may be displayed:" in i:searchInfo(term)
                        else: print(color.YELLOW+'[-] '+color.END+colors[random.randrange(len(colors)-1)]+i+"\n"+color.END)
                else: print(str(i)+'\n')


# Search for Similar Articles
def searchInfo(term):
    final_content = []
    r = requests.get("https://en.wikipedia.org/w/index.php?search="+term)
    if '/wiki/' in r.url:
        getInfo(term)
    else:
        content = r.text
        soup = BeautifulSoup(content,'html.parser')
        content = soup.find_all('a')
        did = soup.find('a',{'id':'mw-search-DYM-suggestion'})
        for i in content:
            if i.get('title') == i.get_text():
                final_content.append(i.get_text())
        final_content = final_content[2:]
        print("Did You Mean: \n")
        if did is not None:
            print(did.get_text())
            print(*final_content[:5],sep ="\n")
        else:
            print(*final_content[:5],sep="\n")
