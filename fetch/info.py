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

def req(term):
    global wikiurl 
    wikiurl = "https://en.m.wikipedia.org/wiki/"+term
    r = requests.get(wikiurl)
    return r.text

def getSummary(term):
    final_content = []
    content = req(term)
    soup = BeautifulSoup(content,'html.parser')
    content = soup.find_all('p') 
    print('\n'+(color.BOLD+str(term)).center(width,"-")+ "\n"+color.END)
    for i in content:
        if i.get_text() == "\n": pass
        else:
            if i('sup'):
                for tag in i('sup'): tag.decompose()
            data = i.get_text()
            final_content.append(data)
            if len(final_content) == 2: break
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
    content = soup.find_all('p') 
    for i in content:
        if i('sup'):
            for tag in i('sup'): tag.decompose()
        data = i.get_text()
        final_content.append(data)
    if "may refer to:" in str(final_content[0]): term = searchInfo(term)
    else:
        if p == True:
            print('\n'+(color.BOLD+str(term)).center(width,"-")+color.END+'\n')
            print(color.BLUE+str(wikiurl).center(width," ")+color.END+'\n')
        if p == False:
            print('\n'+str(term).center(width,"-"))
            print('\n'+str(wikiurl).center(width, " ")+'\n')
        for i in final_content:
            if i == "\n": pass
            else:
                if p == True: print(color.YELLOW+"[-] "+color.END+colors[random.randrange(len(colors)-1)]+i+"\n"+color.END)
                else: print("[-]"+str(i))
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
