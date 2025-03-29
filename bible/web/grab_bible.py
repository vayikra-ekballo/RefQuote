#!/usr/bin/env python3

import json
import requests
from time import sleep
from bs4 import BeautifulSoup
from yield_books import yield_protestant_canon_books


def chunk_out(html):
    soup = BeautifulSoup(html, "html.parser")

    std_text_l = soup.find_all("div", class_="std-text")
    if len(std_text_l) != 1:
        raise Exception(
            "Expected a single <div> with class='std-text'. Got %d." % len(std_text_l)
        )
    std_text = std_text_l[0]

    footnotes_l = soup.find_all("div", class_="footnotes")
    if len(footnotes_l) > 1:
        raise Exception(
            "Expected a single <div> with class='footnotes'. Got %d." % len(footnotes_l)
        )
    footnotes = footnotes_l[0] if len(footnotes_l) == 1 else None

    crossrefs_l = soup.find_all("div", class_="crossrefs hidden")
    if len(crossrefs_l) != 1:
        raise Exception(
            "Expected a single <div> with class='crossrefs hidden'. Got %d."
            % len(footnotes_l)
        )
    crossrefs = crossrefs_l[0] if len(crossrefs_l) == 1 else None

    return {
        "verses_html": str(std_text),
        "footnotes_html": str(footnotes),
        "crossrefs_html": str(crossrefs),
    }


def grab_chapter(book, chapter, translation):
    url = f"https://www.biblegateway.com/passage/?search={book}%20{chapter}&version={translation}"
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    return chunk_out(html)


def grab_bible(translation):
    for book_name, chapter_count in yield_protestant_canon_books():
        chapters = []
        for chapter_number in range(1, chapter_count + 1):
            print(f"Grabbing {book_name} {chapter_number}...")
            json_output = grab_chapter(book_name, chapter_number, translation)
            chapters.append(json_output)
            sleep(0.5)

        assert len(chapters) == chapter_count
        json_output = json.dumps(chapters, indent=4)
        file_name = f"archive/{translation.lower()}/{book_name}.html.json"
        with open(file_name, "w") as f:
            f.write(json_output)


if __name__ == "__main__":
    grab_bible("NIV")
