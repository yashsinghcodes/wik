#!/usr/bin/env python3
import argparse

from wik import info

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", help="Search any topic")
parser.add_argument("-i", "--info", help="Get info on any topic")
parser.add_argument("-q", "--quick", help="Get the summary on any topic")
parser.add_argument(
    "-l", "--lang", help="Get info in your native language (default english)"
)
parser.add_argument(
    "-x", "--rand", help="Get random Wikipedia article", action="store_true"
)

a = parser.parse_args()
if not a.lang: a.lang="EN"

def arguments():
    if a.quick:
        info.getSummary(a.quick, a.lang)
    if a.info:
        info.getInfo(a.info, a.lang)
    if a.search:
        info.searchInfo(a.search, a.lang)
    if a.rand:
        info.getRand(a.lang)
