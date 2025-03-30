#!/usr/bin/env python3

import json
import requests
import warnings
from time import sleep
from bs4 import BeautifulSoup, Comment
from yield_books import yield_protestant_canon_books

warnings.filterwarnings("ignore", category=DeprecationWarning)


def chunk_out(html: str, translation: str):
    soup = BeautifulSoup(html, "html.parser")

    if translation == "NIV":
        std_text_l = soup.find_all("div", class_="std-text")
        if len(std_text_l) != 1:
            raise Exception(
                "Expected a single <div> with class='std-text'. Got %d."
                % len(std_text_l)
            )
        std_text = std_text_l[0]

        footnotes_l = soup.find_all("div", class_="footnotes")
        if len(footnotes_l) > 1:
            raise Exception(
                "Expected a single <div> with class='footnotes'. Got %d."
                % len(footnotes_l)
            )
        footnotes = footnotes_l[0] if len(footnotes_l) == 1 else None

        crossrefs_l = soup.find_all("div", class_="crossrefs hidden")
        if len(crossrefs_l) != 1:
            raise Exception(
                "Expected a single <div> with class='crossrefs hidden'. Got %d."
                % len(footnotes_l)
            )
        crossrefs = crossrefs_l[0] if len(crossrefs_l) == 1 else None

    else:
        std_text_l = soup.find_all("div", class_="result-text-style-normal")
        if len(std_text_l) != 1:
            raise Exception(
                "Expected a single <div> with class='result-text-style-normal'. Got %d."
                % len(std_text_l)
            )
        std_text = std_text_l[0]

        footnotes_l = soup.find_all("div", class_="footnotes")
        if len(footnotes_l) > 1:
            raise Exception(
                "Expected a single <div> with class='footnotes'. Got %d."
                % len(footnotes_l)
            )
        footnotes = footnotes_l[0] if len(footnotes_l) == 1 else None

        if footnotes is not None:
            unwanted_footnotes_div = std_text.find("div", class_="footnotes")
            for comment in std_text.find_all(
                text=lambda text: isinstance(text, Comment)
            ):
                comment.extract()
            unwanted_footnotes_div.extract()

        crossrefs_l = soup.find_all("div", class_="crossrefs hidden")
        if len(crossrefs_l) > 1:
            raise Exception(
                "Expected a single <div> with class='crossrefs hidden'. Got %d."
                % len(footnotes_l)
            )
        crossrefs = crossrefs_l[0] if len(crossrefs_l) == 1 else None

        if crossrefs is not None:
            unwanted_crossrefs_div = std_text.find("div", class_="crossrefs hidden")
            unwanted_crossrefs_div.extract()

    chunks = {"verses_html": str(std_text), "footnotes_html": str(footnotes)}
    if crossrefs is not None:
        chunks["crossrefs_html"] = str(crossrefs)
    return chunks


def grab_chapter(book: str, chapter: int, translation: str):
    url = f"https://www.biblegateway.com/passage/?search={book}%20{chapter}&version={translation}"
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    chunks = chunk_out(html, translation)
    return chunks


def grab_bible(translation: str):
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
    # grab_bible("NIV")
    # grab_bible("NLT")
    grab_bible("ESV")
    # chunks = grab_chapter("Jude", 1, "ESV")
    # print(chunks["verses_html"])
    # print()
    # print(chunks["crossrefs_html"])
    # print()
    # print(chunks["footnotes_html"])
    pass
