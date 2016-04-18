import re
import os.path
import requests
from bs4 import BeautifulSoup

pages = ['http://jagbani.punjabkesari.in/latest.aspx?pageno=1',
         'http://jagbani.punjabkesari.in/latest.aspx?pageno=2',
         'http://jagbani.punjabkesari.in/latest.aspx?pageno=3',
         'http://jagbani.punjabkesari.in/latest.aspx?pageno=4',
         'http://jagbani.punjabkesari.in/latest.aspx?pageno=5']

title = []
url_addr = []
message = []
toCrawl = []


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
    with open('Files/jagbani_crawled_urls.txt', 'a', encoding="utf-8") as f:
        f.write(addr + '\n')


# Check if file exists return true, else create one
def file_exists(fname):
    if not os.path.isfile(fname):
        file = open(fname, 'w', encoding="utf-8")
        file.close()


# Check if url exists in crawled_urls.txt file
def url_exists(url):
    with open('Files/jagbani_crawled_urls.txt', 'r', encoding="utf-8") as f:
        if url in f.read():
            return True
        else:
            return False


# Get news Title and Url from the category page
def get_news_title_and_url(page):
    file_exists('Files/jagbani_crawled_urls.txt')
    g_data = get_soup(page).find_all("span", class_="story")

    for item in g_data:
        if not url_exists(item.contents[1].find("a").get('href')):
            title.append(item.contents[1].find("a").text)
            url_addr.append(item.contents[1].find("a").get('href'))
            toCrawl.append(item.contents[1].find("a").get('href'))


# Get news message from the url
def get_news_message():
    for addr in toCrawl:
        if not url_exists(addr):
            g_data = get_soup(addr).find_all("div", class_="desc")

            for item in g_data:
                # The program can be modified to get articles based on the date
                # The code below displays date like Tuesday, April 19, 2016-12:38 AM
                # print(item.contents[0].find("div", class_="time2").text)

                message.append(item.contents[1].text)


# Combine url, title and message and write it to txt file
def get_full_news():
    file_exists('Files/jagbani_news.txt')
    for i in range(len(url)):
        try:
            # Uncomment the code below to see output in your program
            # print(title[i])
            # print(message[i])
            # print("Source : {}".format(url_addr[i]))
            # print()

            if not url_exists(url_addr[i]):
                with open('Files/jagbani_news.txt', 'a', encoding="utf-8") as f:
                    f.writelines(title[i].strip() + '\n')
                    f.writelines(message[i].strip() + '\n')
                    f.write("Source : {}".format(url_addr[i]) + '\n')
                    f.write('\n')
                    add_to_crawled_list(url_addr[i])
        except IndexError:
            pass


# Get news from urls in the pages list
for url in pages:
    get_news_title_and_url(url)
    get_news_message()
    get_full_news()
