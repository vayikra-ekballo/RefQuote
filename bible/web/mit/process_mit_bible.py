#!/usr/bin/env python3
from bs4 import BeautifulSoup
import json
import re

from yield_chapters import yield_chapters


def process_bible():
    count = 0

    for (book_short_name, chapter, book_full_name) in yield_chapters():
        count += 1
        print(book_full_name, chapter)

    print(f'{count} chapters processed.')


process_bible()

