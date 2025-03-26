#!/usr/bin/env python3

from collections import OrderedDict
from multiprocessing import Pool
from bs4 import BeautifulSoup
import json
import re

def process_1(soup):
    # Extract title and subtitle
    title = soup.find('h3').get_text(strip=True)
    subtitle = soup.find('h4').get_text(strip=True)

    # Extract verses
    verses = []
    current_verse = {
        'number': None,
        'text': ''
    }

    for line_elem in soup.find_all('span', class_=re.compile(r'^text Ps-23-\d+')):
        # Extract verse number
        verse_num_elem = line_elem.find('sup', class_='versenum')
        if verse_num_elem:
            # New verse starts
            if current_verse:
                verses.append(current_verse)
            current_verse = {
                'number': int(verse_num_elem.get_text(strip=True)),
                'text': ''
            }

        # Extract text (excluding verse number)
        line_text = line_elem.get_text(strip=True)
        if verse_num_elem:
            line_text = line_text.replace(verse_num_elem.get_text(strip=True), '').strip()

        # # Add footnotes and crossreferences
        # footnotes = line_elem.find_all('sup', class_='footnote')
        # crossrefs = line_elem.find_all('sup', class_='crossreference')
        #
        # if footnotes:
        #     current_verse['footnotes'] = [
        #         f'[{fn.get_text(strip=True)}]' for fn in footnotes
        #     ]
        #
        # if crossrefs:
        #     current_verse['crossreferences'] = [
        #         f'<{cr.get_text(strip=True)}>'.replace('(', '').replace(')', '')
        #         for cr in crossrefs
        #     ]

        # Accumulate text
        if line_text:
            current_verse['text'] += line_text + ' '

    # Add last verse
    if current_verse:
        verses.append(current_verse)

    # Remove trailing spaces from text
    for verse in verses:
        verse['text'] = verse['text'].strip()

    # Create final JSON structure
    return {
        'title': title,
        'subtitle': subtitle,
        'verses': verses
    }

def process_bible():
    with open('Psalm-23-NIV.html', 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    std_text_l = soup.find_all("div", class_="std-text")
    if len(std_text_l) != 1:
        raise Exception("Expected a single <div> with class='std-text'. Got %d." % len(std_text_l))
    std_text = std_text_l[0]

    footnotes_l = soup.find_all("div", class_="footnotes")
    if len(footnotes_l) > 1:
        raise Exception("Expected a single <div> with class='footnotes'. Got %d." % len(footnotes_l))
    footnotes = footnotes_l[0] if len(footnotes_l) == 1 else None

    crossrefs_l = soup.find_all("div", class_="crossrefs hidden")
    if len(crossrefs_l) > 1:
        raise Exception("Expected a single <div> with class='crossrefs hidden'. Got %d." % len(footnotes_l))
    crossrefs = crossrefs_l[0] if len(crossrefs_l) == 1 else None

    # print(str(std_text))
    # print()
    # print(str(footnotes))
    # print()
    # print(str(crossrefs))

    r = process_1(std_text)
    print(json.dumps(r, indent=4))

if __name__ == "__main__":
    process_bible()

