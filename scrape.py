import argparse
from contextlib import contextmanager
import re
import sys

from bs4 import BeautifulSoup
import requests

def get_page(url):
    result = requests.get(url)
    assert(result.ok)
    assert(result.text)
    return result.text
    
@contextmanager
def html_context(output_filename):
    # Context manager for appending scraped HTML content to a file.
    with open(output_filename, "w", encoding="utf-8") as file_handle:
        file_handle.write("<html><head><title>Combined Pages</title></head><body>\n")
        yield file_handle  # Provide the file object to the caller
        file_handle.write("</body></html>")  # Close the HTML structure after iteration 

def add_page(html_body, file_handle):
    for element in html_body.find_all(attrs={'id': 'pdp-credit-bar'}):
        element.decompose()
    post_propper = html_body.find_all('shreddit-post')
    file_handle.write(str(post_propper) + "\n")
    
def get_body(html_text):
    soup = BeautifulSoup(html_text, features='lxml')
    assert(soup.body)
    return soup.body
    
def get_next(html_body, next_text):
    next_link = None
    for link in html_body.find_all('a'):
        if(link.text.strip() == next_text and link.has_attr('href')):
            next_link = link['href']
            print(f"found next page: {next_link}")
            break
    return next_link
    
def scrape_once(url, next_text, file_handle):
    html_text = get_page(url)
    html_body = get_body(html_text)
    add_page(html_body, file_handle)
    next_link = get_next(html_body, next_text)
    return next_link

def scrape(first_url, next_text, max_pages, output_filename):
    url = first_url
    with html_context(output_filename) as file_handle:
        for idx in range(0, max_pages):
            url = scrape_once(url, next_text, file_handle)
            if not url:
                print(f"Next link not found")
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='the root (first) url to start from')
    parser.add_argument('-n', '--next', default="Next", help='the link to the next page')
    parser.add_argument('-m', '--max', type=int, default="200", help='the max number of pages to scrape')
    parser.add_argument('-o', '--output', default="story.html", help='the output file')
    args = parser.parse_args()
    return scrape(args.url, args.next, args.max, args.output)

if __name__ == "__main__":
    sys.exit(main())
