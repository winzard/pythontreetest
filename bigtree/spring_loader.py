#!/usr/bin/python
          # -*- coding: UTF-8 -*-
__author__ = 'winzard'
__url_to_load__ = 'http://vesna.yandex.ru/astronomy.xml'
from bs4 import BeautifulSoup as soup
from urllib2 import urlopen
import re


def extract_text(container):
    return container.text

def load_single_page():
    page = soup(urlopen(__url_to_load__))
    #print page.get_text
    container = page.find('td', attrs={'class':'text'})
    title = container.find('h1').text

    if title:
        try:
            extracted = re.search(u'«(.*)»', title) # о, блин, UTF-8 жи есть!
            title = extracted.group(1)

        except AttributeError:
            title = 'Хреново ты, Макс, заголовок извлек'

    if not title:
        title = 'Что-то вообще ничего не работает'
    text = '\n'.join(map(extract_text, container.findAll('p')))


    return title.strip('\n'), text

if __name__ == "__main__":
    title, text = load_single_page()
    print title
