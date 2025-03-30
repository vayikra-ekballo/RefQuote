#!/usr/bin/env python3

import re
import json
from multiprocessing import Pool
from bs4 import BeautifulSoup
from yield_books import yield_protestant_canon_books


def process_1(html):
    soup = BeautifulSoup(html, 'html.parser')

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

def grab_bible_html(translation: str) -> dict:
    bible_html = {}

    def get_file_name(translation: str, book_name: str) -> str:
        return f"archive/{translation.lower()}/{book_name}.html.json"

    for book_name, _ in yield_protestant_canon_books():
        file_name = get_file_name(translation, book_name)
        with open(file_name, "r") as f:
            book = json.load(f)
        bible_html[book_name] = book
    return bible_html

def process_bible(translation: str):
    bible_html = grab_bible_html(translation)
    r = process_1(bible_html['Psalms'][23-1]['verses_html'])
    print(json.dumps(r, indent=4))

if __name__ == "__main__":
    process_bible("NIV")
