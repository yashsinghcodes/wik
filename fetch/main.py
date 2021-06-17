import requests
import sys
import os
from bs4 import BeautifulSoup

# TO-Do
"""
[x] make a req function 
[x] make summary function
[ ] More Readable
[ ] Write all argument file
[ ] Add Tile in complete text
[ ] Enjoy It

"""
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
            print("Did You Mean: ")
            term = searchInfo(term)
            #getSummary(term)
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
    print(*final_content,sep ="\n")
    
if __name__ == '__main__':
    try:
        getSummary(sys.argv[1])
    except BaseException:
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
