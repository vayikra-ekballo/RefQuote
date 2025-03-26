#!/usr/bin/env python3

from collections import OrderedDict
from multiprocessing import Pool
from bs4 import BeautifulSoup
import json
import re

def process_1(soup):
    def extract_text_with_notes(tag):
        text = ""
        for elem in tag.descendants:
            if isinstance(elem, str):
                text += elem
            elif elem.name == "sup":
                if "footnote" in elem.get("class", []):
                    text += f'[{elem.get_text(strip=True)}]'
                elif "crossreference" in elem.get("class", []):
                    text += f'<{elem.get_text(strip=True)}>'
        return " ".join(text.split())

    result = {
        "title": soup.find("h3").get_text(strip=True),
        "subtitle": soup.find("h4").get_text(strip=True),
        "verses": []
    }

    for verse in soup.find_all("span", class_=lambda c: c and c.startswith("text Ps-")):
        verse_number_tag = verse.find("sup", class_="versenum")
        if verse_number_tag:
            verse_number = verse_number_tag.get_text(strip=True)
            verse_number_tag.extract()
        else:
            verse_number = ""

        verse_text = extract_text_with_notes(verse)
        result["verses"].append({"verse": verse_number, "text": verse_text})

    return json.dumps(result, indent=4, ensure_ascii=False)

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

    print(process_1(std_text))

if __name__ == "__main__":
    process_bible()

