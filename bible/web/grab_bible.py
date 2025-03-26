#!/usr/bin/env python3

import json
import requests
from bs4 import BeautifulSoup

def chunk_out(html):
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
    if len(crossrefs_l) != 1:
        raise Exception("Expected a single <div> with class='crossrefs hidden'. Got %d." % len(footnotes_l))
    crossrefs = crossrefs_l[0] if len(crossrefs_l) == 1 else None

    return {
        'verses_html': str(std_text),
        'footnotes_html': str(footnotes),
        'crossrefs_html': str(crossrefs)
    }


def grab_chapter(book, chapter, translation):
    url = f"https://www.biblegateway.com/passage/?search={book}%20{chapter}&version={translation}"
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    chunked = chunk_out(html)
    json_output = json.dumps(chunked, indent=4)
    return json_output


def grab_bible():
    json_output = grab_chapter("Psalm", 23, "NIV")
    print(json_output)


if __name__ == "__main__":
    grab_bible()

