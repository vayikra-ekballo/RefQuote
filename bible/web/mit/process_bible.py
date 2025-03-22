#!/usr/bin/env python3

from collections import OrderedDict
from multiprocessing import Pool
from bs4 import BeautifulSoup
import json
import re

from yield_chapters import yield_chapters, RawBibleChapter, yield_books


def extract_html_portions(html_content):
    m = re.search(r'<OL>.*?</OL>', html_content, re.DOTALL)
    s = m.start() + len('<OL>')
    e = m.end() - len('</OL>')
    footnotes_html = html_content[s:e].strip()

    m = re.search(r'</DL>.*?</DL>', html_content, re.DOTALL)
    s = m.start() + len('</DL>')
    e = m.end() - len('</DL>')
    verses_plus_title_html = html_content[s:e].strip()

    soup = BeautifulSoup(verses_plus_title_html, 'html.parser')
    if soup.find('b'):
        title = soup.find('b').get_text(strip=True)
    else:
        raise Exception("Unknown Title")

    # Extract just the verses
    m = re.search(r'<DL COMPACT>.*?', verses_plus_title_html, re.DOTALL)
    s = m.start() + len('<DL COMPACT>')
    verses_html = verses_plus_title_html[s:].strip()

    return {
        'title': title,
        'verses_html': verses_html,
        'footnotes_html': footnotes_html
    }


def footnotes_html_to_array(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = []
    
    for li in soup.find_all('li'):
        text = ''
        for elem in li.contents:  # Use contents instead of descendants to avoid repetition
            if isinstance(elem, str):
                text += elem
            elif elem.name == 'i':
                text += f'*{elem.get_text()}*'
            elif elem.name == 'a':  # Handle anchor tags separately
                text += ''.join(
                    f'*{sub_elem.get_text()}*' if sub_elem.name == 'i' else sub_elem for sub_elem in elem.contents
                )
        
        text = re.sub(r'^\[\d+\]\s*', '', text.strip())  # Remove leading [number]
        result.append(text)
    
    return result


def verses_html_iterator(html):
    # print(html)

    # Use regex to find all verse sections (DT and DD pairs)
    pattern = r'<DT>(\d+)\s*<DD>(.*?)(?=<DT>|$)'
    matches = re.findall(pattern, html, re.DOTALL)
    
    # Process each match to clean HTML and create structured data
    for number, content in matches:
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract text and remove unnecessary whitespace
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text).strip()

        if '\x1a' in text:
            text = text.replace('\x1a', '').strip()
        
        yield (int(number), text)


def process_verses(html):
    verses = dict()
    subheading = None

    for (vn, verse) in verses_html_iterator(html):
        if vn not in verses:
            verses[vn] = verse
        else:
            if vn == 1:
                subheading = verses[1]
                verses[1] = verse
            else:
                raise Exception('Repeating verse: %d.' % vn)

    verses_array = []
    skipped_verse_numbers = []
    for i in range(1, len(verses) + 1):
        if i not in verses:
            skipped_verse_numbers.append(i)
        else:
            verses_array.append(verses[i])

    return (subheading, verses_array, skipped_verse_numbers)


class BibleChapter(RawBibleChapter):
    def __init__(self, ch: RawBibleChapter, log=False):
        super().__init__(ch.code_name, ch.chapter, ch.full_name)
        if log == True:
            print('Processing %s %d...' % (ch.full_name, ch.chapter))
        
        portions = extract_html_portions(ch.html)
        self.title = portions['title']
        self.footnotes = footnotes_html_to_array(portions['footnotes_html'])
        self.subheading, self.verses, self.skipped_verse_numbers = process_verses(portions['verses_html'])

    def display(self):
        print('Title:', self.title, '\n')
        print('Subheading:', self.subheading, '\n')
        print('Verses:', self.verses, '\n')
        if len(self.skipped_verse_numbers) > 0:
            print('Skipped verses:', self.skipped_verse_numbers)
        print('Footnotes:', self.footnotes, '\n')


def process_chapter(raw_chapter: RawBibleChapter) -> BibleChapter:
    return BibleChapter(raw_chapter)


def process_bible():
    raw_chapters = list(yield_chapters())

    total_chapters_count = len(raw_chapters)
    assert len(raw_chapters) == 1189

    with Pool() as p:
      chapters = p.map(process_chapter, raw_chapters)  

    bible = {
        'books': OrderedDict()
    }

    for (code_name, chapter_count, full_name) in yield_books():
        for chapter in range(1, chapter_count + 1):
            if full_name not in bible['books']:
                bible['books'][full_name] = []
            bible['books'][full_name].append(None)

    for ch in chapters:
        chapter = OrderedDict()
        chapter["title"] = ch.title
        if ch.subheading is not None:
            chapter['subheading'] = ch.subheading
        chapter["verses"] = ch.verses
        if len(ch.skipped_verse_numbers) > 0:
            chapter['skippedVerseNumbers'] = ch.skipped_verse_numbers
        chapter["footnotes"] = ch.footnotes

        bible['books'][ch.full_name][ch.chapter-1] = chapter

    bible_json = json.dumps(bible, indent=4)
    output_json_path = '../../json/mit.json'
    with open(output_json_path, 'w') as f:
        f.write(bible_json)

    print('Done. Written to: %s' % output_json_path)


if __name__ == "__main__":
    process_bible()

