# Retrieves a url from the user to act as a seed to crawl finding all urls associated with that page
# and returns a dictionary of its
import web_scraper
import poodle
import urllib2
import ssl
import sys

# required to gain access to https urls on the school server from home
ssl._create_default_https_context = ssl._create_unverified_context

crawled_graph = {}

def get_url():
    # ask for a URL to crawl e.g. https://dunluce.infc.ulst.ac.uk/d12wo/Web/B3/test_index.html
    while True:
        url_to_crawl = raw_input(" Enter a URL to crawl (-end to exit to menu) \n")
        url_to_crawl = url_to_crawl.strip() # remove whitespace from start and end if any
        url_to_crawl = url_to_crawl.lower()  # convert to lowercase

        if url_to_crawl[:7] == "http://" or url_to_crawl[:8] == "https://":  # check if URL is http or https
            if url_to_crawl[-1] == "/":  # remove forward slash from the end
                url_to_crawl = url_to_crawl[:-1]
                break
            else:
                break
        elif url_to_crawl == "-end":
            poodle.init_menu_options()
        else:
            print " URL must begin with http:// or https://\n"

    crawl_url(url_to_crawl)

def get_depth():
    while True:
        try:
            max_depth = int(raw_input(" Enter the depth {1-10} you want to crawl this URL: "))
        except ValueError:
            print " Not a number -- Try Again."
        else:
            if 1 <= max_depth < 11:
                break
            else:
                print " Out of range {1-10} -- Try Again."

    return max_depth

def crawl_url(seed):
    MAX_DEPTH = get_depth()  # gets to interesting.html if set at 5. Limiting depth allows the search to be controlled
    to_crawl = [seed]
    crawled = []

    while to_crawl and len(crawled) < MAX_DEPTH:
        unique_urls = []
        url = to_crawl.pop()
        crawled.append(url)

        # extract all undiscovered links in the source HTML of the current page
        # and merge those links with the to_crawl list.
        new_links = get_all_new_links_on_page(url, crawled, unique_urls)
        to_crawl = list(set(to_crawl) | set(new_links))

        # graph of unique urls
        crawled_graph[url] = unique_urls

    # print urls after the url has been crawled
    for url in crawled_graph:
        print url

    # pass graph to scrape it
    web_scraper.scrape_page(crawled_graph)


def get_all_new_links_on_page(page, prev_links, unique_urls):
    response = urllib2.urlopen(page)
    html = response.read()

    links, pos, all_found = [], 0, False
    while not all_found:
        atag = html.find("<a href=", pos)
        if atag > -1:
            href = html.find('"', atag + 1)
            end_href = html.find('"', href + 1)
            url = html[href + 1:end_href]
            if url[:8] == "https://" or url[:7] == "http://":
                if url[-1] == "/":
                    url = url[:-1]
                if not url in links and not url in prev_links:
                    links.append(url)
                if url not in unique_urls:
                    unique_urls.append(url)
            close_tag = html.find("</a>", atag)
            pos = close_tag + 1
        else:
            all_found = True
    return links



def get_graph():
    return crawled_graph

