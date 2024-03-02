# Andre Rodriguez
# andrerod
import sys
import os
import operator
import pdb

def compute_page_rank(stats):
    """Calculate Page Ranks."""
    stats['urls'] = {}
    stats['in'] = {}
    stats['out'] = {}
    stats['ranks'] = {}
    stats['num_sites'] = 0
    url_str = ''
    diff = 0
    crawler_output = str(sys.argv[1])
    links_output = str(sys.argv[2])
    conv_thres = float(sys.argv[3])

    with open(crawler_output, 'r') as crawled_sites:
        for line in crawled_sites:
            line = line.replace('\n','')
            # 0.25 initial value for all URLs
            stats['num_sites'] += 1
            stats['urls'][line] = 0.25
            stats['in'][line] = list()
            stats['out'][line] = list()
    # breakpoint()
    with open(links_output, 'r', encoding='UTF-8') as edges:
        for links in edges:
            links = links.replace('\n','')
            links = links.split(" ")
            sourceURL, URL = links[0], links[1]
            # breakpoint()
            if sourceURL in stats['urls'] and URL in stats['urls'] and not sourceURL == URL:
                if not sourceURL in stats['in'][URL]:
                    stats['in'][URL].append(sourceURL)
                if not URL in stats['out'][sourceURL]:
                    stats['out'][sourceURL].append(URL)
    # breakpoint()
    while diff < conv_thres:
        diff = 0
        for url in stats['urls']:
            i = 0
            # stats['ranks'][url] = (0.15 / len(stats['urls'])) / (0.85 * sum([(stats['urls'][link] / len(stats['out'][link])) for link in stats['in'][url]]))
            n1 = (0.15 / len(stats['urls']))
            n2 = 0
            for link in stats['in'][url]:
                n2 += stats['urls'][link] / len(stats['out'][link])
            stats['ranks'][url] = n1 + 0.85 * n2
            curr_diff = abs(stats['urls'][url] - stats['ranks'][url])
            diff = curr_diff if diff < curr_diff else diff
            i += 1
        stats['urls'] = stats['ranks'].copy()
    



# The pagerank.py program should run with the following:
# python3 pagerank.py crawler.output links.output 0.001
if __name__ == '__main__':
    """Main driver for pagerank.py"""
    stats = {}
    compute_page_rank(stats)
    stats['urls'] = sorted(stats['urls'].items(), key=operator.itemgetter(1), reverse=True)
    with open('pagerank.output', 'w', encoding='UTF-8') as w:
        for url in stats['urls']:
            w.write(str(url[0]) + " " + str(url[1]) + '\n')
