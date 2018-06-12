#!/usr/bin/env python3

import os

from sh import wget

def gen_url(book, chapter):
    return f"http://web.mit.edu/jywang/www/cef/Bible/NIV/NIV_Bible/{book}+{chapter}.html"

def process_output(line):
    print(line, end='')

seen = set()

def grab_chapter(book, chapter):
    global seen
    filename = f"{book}+{chapter}.html"
    if os.path.exists(filename):
        if filename in seen:
            raise "Attempt to retrieve same chapter again"
        seen.add(filename)

        print('Already exists:', book, chapter)
        return True

    print('Downloading:', book, chapter)
    wget(gen_url(book, chapter), _out=process_output, _err=process_output)
    return True

def grab_boook(book, chapter_count):
    count = 0
    for chapter in range(1, chapter_count + 1):
        if grab_chapter(book, chapter):
            count += 1
    print()
    return count

def grab_bible():
    count = 0

    # Old Testament:

    count += grab_boook('GEN', 50)
    count += grab_boook('EXOD', 40)
    count += grab_boook('LEV', 27)
    count += grab_boook('NUM', 36)
    count += grab_boook('DEUT', 34)

    count += grab_boook('JOSH', 24)
    count += grab_boook('JUDG', 21)
    count += grab_boook('RUTH', 4)

    count += grab_boook('1SAM', 31)
    count += grab_boook('2SAM', 24)

    count += grab_boook('1KGS', 22)
    count += grab_boook('2KGS', 25)

    count += grab_boook('1CHRON', 29)
    count += grab_boook('2CHRON', 36)

    count += grab_boook('EZRA', 10)
    count += grab_boook('NEH', 13)
    count += grab_boook('ESTH', 10)
    count += grab_boook('JOB', 42)

    count += grab_boook('PS', 150)

    count += grab_boook('PROV', 31)
    count += grab_boook('ECC', 12)

    count += grab_boook('SONG', 8)

    count += grab_boook('ISA', 66)
    count += grab_boook('JER', 52)

    count += grab_boook('LAM', 5)

    count += grab_boook('EZEK', 48)
    count += grab_boook('DAN', 12)

    count += grab_boook('HOSEA', 14)
    count += grab_boook('JOEL', 3)
    count += grab_boook('AMOS', 9)
    count += grab_boook('OBAD', 1)
    count += grab_boook('JONAH', 4)
    count += grab_boook('MICAH', 7)
    count += grab_boook('NAHUM', 3)
    count += grab_boook('HAB', 3)
    count += grab_boook('ZEPH', 3)
    count += grab_boook('HAG', 2)
    count += grab_boook('ZECH', 14)
    count += grab_boook('MAL', 4)

    # New Testament:

    count += grab_boook('MATT', 28)
    count += grab_boook('MARK', 16)
    count += grab_boook('LUKE', 24)
    count += grab_boook('JOHN', 21)

    count += grab_boook('ACTS', 28)
    count += grab_boook('ROM', 16)

    count += grab_boook('1COR', 16)
    count += grab_boook('2COR', 13)

    count += grab_boook('GAL', 6)
    count += grab_boook('EPH', 6)
    count += grab_boook('PHIL', 4)
    count += grab_boook('COL', 4)

    count += grab_boook('1THES', 5)
    count += grab_boook('2THES', 3)

    count += grab_boook('1TIM', 6)
    count += grab_boook('2TIM', 4)

    count += grab_boook('TIT', 3)
    count += grab_boook('PHILEM', 1)

    count += grab_boook('HEB', 13)
    count += grab_boook('JAS', 5)
    count += grab_boook('1PET', 5)
    count += grab_boook('2PET', 3)
    count += grab_boook('1JOHN', 5)
    count += grab_boook('2JOHN', 1)
    count += grab_boook('3JOHN', 1)
    count += grab_boook('JUDE', 1)

    count += grab_boook('REV', 22)

    print(f'{count} chapters retrieved.')

grab_bible()
