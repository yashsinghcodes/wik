import argparse
from fetch.main import searchInfo


parser = argparse.ArgumentParser()
parser.add_argument("-s","--search",help="Search your topic")

args = parser.parse_args()

if args.Output:
    searchInfo(args.Output)