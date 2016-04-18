import re
import requests
from bs4 import BeautifulSoup

url = 'http://www.babushahi.com/news.php?region=punjab#news'


# Get BeautifulSoup Object 'soup'
def get_soup(page):
    url = page
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36'}

    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


# Get latest news from babushahi.com
def get_news(url):
    g_data = get_soup(url).find_all(id="poll")
    for item in g_data:
        try:
            url = (
            item.contents[3].find(href=re.compile("^http://www.babushahi.com/news-detail.php?")).get('href')).strip()
            title = (item.contents[3].find(href=re.compile("^http://www.babushahi.com/news-detail.php?")).text).strip()
            message = (item.contents[9].find("div", class_="sarkar_content").contents[1].next_sibling).strip()

            # print(title)
            # print(message)
            # print("Source: {}".format(url))
            # print()
            write_to_file(title, message, url)
        except TypeError and AttributeError:
            pass


# Write news to txt file
def write_to_file(title, message, addr):
    with open("Files/babushahi_news.txt", 'a', encoding='utf-8') as f:
        f.write(title + '\n')
        f.write(message + '\n')
        f.write("Source: {}".format(addr) + '\n')
        f.write('\n')


get_news(url)
