import argparse
from contextlib import contextmanager
import re
import sys
import time

from bs4 import BeautifulSoup
import requests

def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print(f"{url} returned status code {response.status_code}")
        assert(response.ok)
    assert(response.text)
    return response.text
    
@contextmanager
def html_context(output_format, output_filename):
    # Context manager for appending scraped HTML content to a file.
    with open(output_filename, "w", encoding="utf-8") as file_handle:
        if(output_format.lower() == "html"):
            file_handle.write("<html><head><title>Combined Pages</title></head><body>\n")
        yield file_handle  # Provide the file object to the caller
        if(output_format.lower() == "html"):
            file_handle.write("</body></html>")  # Close the HTML structure after iteration 

def extract_post(html_body):
    for element in html_body.find_all(attrs={'id': 'pdp-credit-bar'}):
        element.decompose()
    for element in html_body.find_all('shreddit-post-flair'):
        element.decompose()
    for element in html_body.find_all('button'):
        element.decompose()
    return html_body.find_all('shreddit-post')

def convert_to_plaintext(post_proper):
    text = ""
    for element in post_proper:
        text += (str(element.get_text()) + "\n")
    return text

def add_page(html_body, output_format, file_handle):
    post_propper = extract_post(html_body)
    if(output_format.lower() == "plaintext"):
        post_propper = convert_to_plaintext(post_propper)
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
    
def scrape_once(url, next_text, output_format, file_handle):
    html_text = get_page(url)
    html_body = get_body(html_text)
    add_page(html_body, output_format, file_handle)
    next_link = get_next(html_body, next_text)
    return next_link

def scrape(first_url, next_text, max_pages, output_format, output_filename, sleep_secs):
    url = first_url
    with html_context(output_format, output_filename) as file_handle:
        for idx in range(0, max_pages):
            url = scrape_once(url, next_text, output_format, file_handle)
            if not url:
                print(f"Next link not found")
                break
            time.sleep(sleep_secs)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='the root (first) url to start from')
    parser.add_argument('-n', '--next', default="Next", help='the link to the next page')
    parser.add_argument('-m', '--max', type=int, default="1000", help='the max number of pages to scrape')
    parser.add_argument('-f', '--format', default="plaintext", choices=["plaintext", "html"], help='output format')
    parser.add_argument('-o', '--output', default="story.txt", help='the output file')
    parser.add_argument('-s', '--sleep', type=int, default="1", help='how many seconds to sleep between each request')
    args = parser.parse_args()
    return scrape(args.url, args.next, args.max, args.format, args.output, args.sleep)

if __name__ == "__main__":
    sys.exit(main())
