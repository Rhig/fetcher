#!/usr/bin/env python

import argparse
import urllib.request
import bs4 as bs

from metadata import Metadata

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls', nargs='+')
    parser.add_argument('--metadata', action='store_true', required=False)
    parser.add_argument("--metadata_filepath", action="store", required=False)
    return parser.parse_args()

def preprocess_urls(urls):
    return [url.rstrip("/") for url in urls]

def open_url(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    return urllib.request.urlopen( req )

def validate_urls(urls):
    for url in urls:
        try:
            open_url(url)
        except Exception as e:
            raise ValueError(f"Error trying to open url {url}.\n{e}")
        
def init_metadata(args):
    metadata_kwargs = {}
    if args.metadata_filepath:
        metadata_kwargs["metadata_filepath"] = args.metadata_filepath
    return Metadata(**metadata_kwargs)

def url_to_filename(url):
    split_by_colon_doubleslash = url.split("://")
    if len(split_by_colon_doubleslash) > 1:
        url = split_by_colon_doubleslash[1]
    return url.replace("/", "%") + ".html"

def download_pages(urls, url_filenames, metadata):
    for url, url_filename in zip(urls, url_filenames):
        source = open_url(url).read()
        soup = bs.BeautifulSoup(source, 'lxml')
        with open(url_filename, "w") as f:
            f.write(soup.get_text())
        num_of_links = len(soup.find_all('a'))
        num_of_images = len(soup.find_all('img'))
        metadata.update_page_metadata(url, num_of_links, num_of_images)

def display_metadata(urls, metadata):
    for url in urls:
        print(f"site: {url}")
        page_metadata = metadata.get_page_metadata(url)
        if not page_metadata:
            print(f"-E- No metadata found for site {url}.\n")
            continue
        for key, value in page_metadata.items():
            print(f"{key}: {value}")
        print()

def main(args):
    urls = preprocess_urls(args.urls)
    validate_urls(urls)
    metadata = init_metadata(args)
    url_filenames = [url_to_filename(url) for url in urls]
    if args.metadata:
        display_metadata(urls, metadata)
    else:
        download_pages(urls, url_filenames, metadata)

if __name__ == '__main__':
    args = get_arguments()
    main(args)
