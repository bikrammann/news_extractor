import re
import os.path
import requests
from bs4 import BeautifulSoup

toCrawl = []
title = []
url = []
msg = []

# List of news categories
categories = ['http://www.punjabspectrum.news/category/breaking',
              'http://www.punjabspectrum.news/category/international',
              'http://www.punjabspectrum.news/category/misc',
              'http://www.punjabspectrum.news/category/india',
              'http://www.punjabspectrum.news/category/punjab',
              'http://www.punjabspectrum.news/category/sikh-world']


# Get BeautifulSoup Object 'soup'
def get_soup(page):
    url = page
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36'}

    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


# Add urls to the list that we have already crawled, to avoid duplicates
def add_to_crawled_list(addr):
    with open('Files/crawled_urls.txt', 'a', encoding="utf-8") as f:
        f.write(addr + '\n')


# Check if file exists return true, else create one
def file_exists(fname):
    if not os.path.isfile(fname):
        file = open(fname, 'w', encoding="utf-8")
        file.close()

# Check if url exists in crawled_urls.txt file
def url_exists(url):
    with open('Files/crawled_urls.txt', 'r', encoding="utf-8") as f:
        if url in f.read():
            return True
        else:
            return False


# Get news Title and Url from the category page
def get_news_title_and_url(page):
    file_exists('Files/crawled_urls.txt')
    g_data = get_soup(page).find_all("h2", class_="post-title")

    for item in g_data:
        if not url_exists(item.contents[0].get('href')):
            escapedT = re.sub(r'[^\w\s]', '', item.contents[0].text)
            title.append(escapedT)
            url.append(item.contents[0].get('href'))
            toCrawl.append(item.contents[0].get('href'))


# Get news message from the url
def get_news_message():
    for addr in toCrawl:
        if not url_exists(addr):
            g_data = get_soup(addr).find_all("div", class_="entry clearfix")

            for item in g_data:
                msg.append(item.contents[1].find_all('p')[0].text)


# Combine title, url and message and add to news.txt
def get_full_news():
    file_exists('Files/news.txt')
    for i in range(len(url)):
        try:
            # print(title[i])
            # print(msg[i])
            # print("Source : {}".format(url[i]))
            # print()
            if not url_exists(url[i]):
                with open('Files/news.txt', 'a', encoding="utf-8") as f:
                    f.writelines(title[i] + '\n')
                    f.writelines(msg[i] + '\n')
                    f.write("Source : {}".format(url[i]) + '\n')
                    f.write('\n')
                    add_to_crawled_list(url[i])
        except IndexError:
            print("Warning: This news already exists")
            print()


# Get news from all the categories in the categories list
for category in categories:
    get_news_title_and_url(category)
    get_news_message()
    get_full_news()
