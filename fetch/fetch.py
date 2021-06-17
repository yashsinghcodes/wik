import argparse
import main


parser = argparse.ArgumentParser()
parser.add_argument("-s","--search",help="Search any topic")
parser.add_argument("-i","--info",help="Get info on any topic(Use correct name)")

a = parser.parse_args()

if a.search:
    main.searchInfo(a.search)
if a.info:
    main.getInfo(a.info)