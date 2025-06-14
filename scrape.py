import argparse
import re
import sys

from bs4 import BeautifulSoup
import requests

def get_url(url):
    result = requests.get(url)
    assert(result.ok)
    return result.text
    
def get_next(html_text, next_text):
    soup = BeautifulSoup(html_text, features='lxml').find_all('a')
    next_link = None
    for link in soup:
        if(link.has_attr('href') and link.text.strip() == next_text):
            next_link = link['href']
            break
    return next_link
    
def scrape_once(url, next_text):
    html_text = get_url(url)
    next_link = get_next(html_text, next_text)
    return next_link

def scrape(first_url, next_text, max_pages):
    url = first_url
    for idx in range(0, max_pages):
        url = scrape_once(url, next_text)
        print(url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='the root (first) url to start from')
    parser.add_argument('-n', '--next', default="Next", help='the link to the next page')
    parser.add_argument('-m', '--max', type=int, default="200", help='the max number of pages to scrape')
    args = parser.parse_args()
    return scrape(args.url, args.next, args.max)

if __name__ == "__main__":
    sys.exit(main())
