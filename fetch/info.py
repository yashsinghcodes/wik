import requests
import sys
import os
from bs4 import BeautifulSoup
# TO-Do
"""
[x] make a req function 
[x] make summary function
[ ] More Readable
[x] Write all argument file
[ ] Add Tile in complete text
[ ] Enjoy It

"""
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

def req(term):
    r = requests.get("https://en.m.wikipedia.org/wiki/"+term)
    return r.text

def getSummary(term):
    final_content = []
    content = req(term)
    soup = BeautifulSoup(content,'html.parser')
    content = soup.find_all('p') 
    for i in content:
        if i('sup'):
            for tag in i('sup'):
                tag.decompose()
        data = i.get_text()
        final_content.append(data)
    if "may refer to:" in str(i):
        print("Did You Mean: ")
        term = searchInfo(term)
    else:
        print(final_content[2])
        print(final_content[3])

def getInfo(term):
    final_content = []
    content = req(term)
    soup = BeautifulSoup(content,'html.parser')
    content = soup.find_all('p') 
    for i in content:
        if i('sup'):
            for tag in i('sup'):
                tag.decompose()
        data = i.get_text()
        final_content.append(data)
    for i in final_content:
        if "may refer to:" in str(i):
            term = searchInfo(term)
        else:
            print(i +"\n")

def searchInfo(term):
    final_content = []
    content = req(term)
    soup = BeautifulSoup(content,'html.parser')
    content = soup.find_all('a')
    for i in content:
        if i.get('title') == i.get_text():
            final_content.append(i.get_text())
    final_content = final_content[2:]
    print("Did You Mean: \n")
    print(*final_content,sep ="\n")