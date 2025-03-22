#!/usr/bin/env python3
from bs4 import BeautifulSoup
import json
import re


def process_chapter(book, chapter):
    return True


def process_book(book, chapter_count):
    count = 0
    for chapter in range(1, chapter_count + 1):
        if process_chapter(book, chapter):
            count += 1
    return count


def process_bible():
    count = 0

    # Old Testament:

    count += process_book('GEN', 50)
    count += process_book('EXOD', 40)
    count += process_book('LEV', 27)
    count += process_book('NUM', 36)
    count += process_book('DEUT', 34)

    count += process_book('JOSH', 24)
    count += process_book('JUDG', 21)
    count += process_book('RUTH', 4)

    count += process_book('1SAM', 31)
    count += process_book('2SAM', 24)

    count += process_book('1KGS', 22)
    count += process_book('2KGS', 25)

    count += process_book('1CHRON', 29)
    count += process_book('2CHRON', 36)

    count += process_book('EZRA', 10)
    count += process_book('NEH', 13)
    count += process_book('ESTH', 10)
    count += process_book('JOB', 42)

    count += process_book('PS', 150)

    count += process_book('PROV', 31)
    count += process_book('ECC', 12)

    count += process_book('SONG', 8)

    count += process_book('ISA', 66)
    count += process_book('JER', 52)

    count += process_book('LAM', 5)

    count += process_book('EZEK', 48)
    count += process_book('DAN', 12)

    count += process_book('HOSEA', 14)
    count += process_book('JOEL', 3)
    count += process_book('AMOS', 9)
    count += process_book('OBAD', 1)
    count += process_book('JONAH', 4)
    count += process_book('MICAH', 7)
    count += process_book('NAHUM', 3)
    count += process_book('HAB', 3)
    count += process_book('ZEPH', 3)
    count += process_book('HAG', 2)
    count += process_book('ZECH', 14)
    count += process_book('MAL', 4)

    # New Testament:

    count += process_book('MATT', 28)
    count += process_book('MARK', 16)
    count += process_book('LUKE', 24)
    count += process_book('JOHN', 21)

    count += process_book('ACTS', 28)
    count += process_book('ROM', 16)

    count += process_book('1COR', 16)
    count += process_book('2COR', 13)

    count += process_book('GAL', 6)
    count += process_book('EPH', 6)
    count += process_book('PHIL', 4)
    count += process_book('COL', 4)

    count += process_book('1THES', 5)
    count += process_book('2THES', 3)

    count += process_book('1TIM', 6)
    count += process_book('2TIM', 4)

    count += process_book('TIT', 3)
    count += process_book('PHILEM', 1)

    count += process_book('HEB', 13)
    count += process_book('JAS', 5)
    count += process_book('1PET', 5)
    count += process_book('2PET', 3)
    count += process_book('1JOHN', 5)
    count += process_book('2JOHN', 1)
    count += process_book('3JOHN', 1)
    count += process_book('JUDE', 1)

    count += process_book('REV', 22)

    print(f'{count} chapters processed.')


process_bible()

