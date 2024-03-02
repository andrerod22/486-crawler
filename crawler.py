# Andre Rodriguez
# andrerod

import os
import sys
import requests
import bs4
import pdb

entrance_domains = [
        'eecs.umich',
        'eecs.engin.umich',
        'ece.engin.umich',
        'cse.engin.umich'
    ]

def valid_source(potential_source):
    """Verifies source in anchor tag."""
    # breakpoint()
    in_domain = False
    for domain in entrance_domains:
        if domain in potential_source:
            in_domain = True
            break

    if in_domain:
        if 'https://' in potential_source:
            return potential_source
        parsed_source = potential_source.split('//')
        parsed_source = parsed_source[1] if len(parsed_source) > 1 else None
        if not parsed_source: return None
        parsed_source = parsed_source.replace('www.','',1) if 'www.' in parsed_source else parsed_source
        if not parsed_source.endswith('/'): parsed_source += '/'
        potential_source = 'http://'
        return potential_source + parsed_source

# Note: This function name is pretty specific, but we can expand the crawler
#       To more general cases over the web later. 
def crawl_umich(crawler):
    "Crawls umich engineering website. "
    #prev_urls links
    seed = []
    max_urls = sys.argv[2]
    #frontier = []
    # TOO SLOW 
    # crawler['frontier'] = []
    frontier = []
    # TOO SLOW
    crawler['prev_urls'] = []
    # crawler['links'] = []
    url = ''
    # A) DONE: Start w/ seed
    with open(sys.argv[1], 'r') as input:
        seed = [line.replace('\n', '') for line in input]
    if len(seed) == 1: seed = seed[0]
    # B) DONE: Perform a Web Tranversal via breadth-first strategy (HTML sites only)
        # i) Verify if url is valid along with the page:
    with open('links.output', 'w', encoding='UTF-8') as w:
        for i in range(int(max_urls)):
            # breakpoint()
            url = seed if i == 0 else frontier.pop(0)
            try:
                fetched_page = requests.get(url, headers= {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4867.0 Safari/537.36 Edg/100.0.1167.0"
                    })

                if fetched_page == None: continue
            except:
                continue
            # breakpoint()
            if 'text/html' in fetched_page.headers['content-type'] and fetched_page.url not in crawler['prev_urls']:
                # C) DONE: Keep track of traversed URLS
                    # i) No duplicates --> set --> set()
                    # ii) No cycles 
                crawler['prev_urls'].append(url)
                crawler['prev_urls'] = list(set(crawler['prev_urls']))
                # ii) Search through the entire documents 'a' characters
                for a in bs4.BeautifulSoup(fetched_page.text, 'html.parser').find_all('a'):
                    # iii) Verify that the 'a' character we are on is an anchor tag:
                    anchor_tag = a.get('href')
                    if anchor_tag:
                        # Add the url and visit it in the next iteration DO NOT add prev_urls
                        potential_source = requests.compat.urljoin(url, anchor_tag) if anchor_tag.startswith('/') else anchor_tag

                        # Add potential source to frontier if
                            # valid_source returns true
                            # the source is not in frontiers, nor prev_urls
                        
                        if valid_source(potential_source):
                            pair = url + ' ' + potential_source
                            # crawler['links'].append(pair)
                            w.write(str(pair) + '\n')
                            if potential_source not in frontier and potential_source not in crawler['prev_urls']:
                                #crawler['frontier'].append(potential_source)
                                frontier.append(potential_source)
                    else:
                        continue
    



# The crawler.py program should run with the following:
# python3 crawler.py myseedURL.txt 2000
if __name__ == '__main__':
    """Main driver for crawler.py"""
    crawled_sites = {}
    crawl_umich(crawled_sites)
    breakpoint()
    # D) DONE: Write crawler.output
    with open('crawler.output', 'w', encoding='UTF-8') as w:
        for url in crawled_sites['urls']:
            w.write(str(url) + '\n')

    # E) DONE: Write links.output
    # with open('links.output', 'w', encoding='UTF-8') as w:
        # for edge in crawled_sites['links']:
            # w.write(str(edge) + '\n')
