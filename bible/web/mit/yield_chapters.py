
def yield_books():
    # Old Testament:

    yield ('GEN', 50, 'Genesis')
    yield ('EXOD', 40, 'Exodus')
    yield ('LEV', 27, 'Leviticus')
    yield ('NUM', 36, 'Numbers')
    yield ('DEUT', 34, 'Deuteronomy')

    yield ('JOSH', 24, 'Joshua')
    yield ('JUDG', 21, 'Judges')
    yield ('RUTH', 4, 'Ruth')

    yield ('1SAM', 31, '1 Samuel')
    yield ('2SAM', 24, '2 Samuel')

    yield ('1KGS', 22, '1 Kings')
    yield ('2KGS', 25, '2 Kings')

    yield ('1CHRON', 29, '1 Chronicles')
    yield ('2CHRON', 36, '2 Chronicles')

    yield ('EZRA', 10, 'Ezra')
    yield ('NEH', 13, 'Nehemiah')
    yield ('ESTH', 10, 'Esther')
    yield ('JOB', 42, 'Job')

    yield ('PS', 150, 'Psalms')

    yield ('PROV', 31, 'Proverbs')
    yield ('ECC', 12, 'Ecclesiastes')

    yield ('SONG', 8, 'Song of Songs')

    yield ('ISA', 66, 'Isaiah')
    yield ('JER', 52, 'Jeremiah')

    yield ('LAM', 5, 'Lamentations')

    yield ('EZEK', 48, 'Ezekiel')
    yield ('DAN', 12, 'Daniel')

    yield ('HOSEA', 14, 'Hosea')
    yield ('JOEL', 3, 'Joel')
    yield ('AMOS', 9, 'Amos')
    yield ('OBAD', 1, 'Obadiah')
    yield ('JONAH', 4, 'Jonah')
    yield ('MICAH', 7, 'Micah')
    yield ('NAHUM', 3, 'Nahum')
    yield ('HAB', 3, 'Habakkuk')
    yield ('ZEPH', 3, 'Zephaniah')
    yield ('HAG', 2, 'Haggai')
    yield ('ZECH', 14, 'Zechariah')
    yield ('MAL', 4, 'Malachi')

    # New Testament:

    yield ('MATT', 28, 'Matthew')
    yield ('MARK', 16, 'Mark')
    yield ('LUKE', 24, 'Luke')
    yield ('JOHN', 21, 'John')

    yield ('ACTS', 28, 'Acts')
    yield ('ROM', 16, 'Romans')

    yield ('1COR', 16, '1 Corinthians')
    yield ('2COR', 13, '2 Corinthians')

    yield ('GAL', 6, 'Galatians')
    yield ('EPH', 6, 'Ephesians')
    yield ('PHIL', 4, 'Philippians')
    yield ('COL', 4, 'Colossians')

    yield ('1THES', 5, '1 Thessalonians')
    yield ('2THES', 3, '2 Thessalonians')

    yield ('1TIM', 6, '1 Timothy')
    yield ('2TIM', 4, '2 Timothy')

    yield ('TIT', 3, 'Titus')
    yield ('PHILEM', 1, 'Philemon')

    yield ('HEB', 13, 'Hebrews')
    yield ('JAS', 5, 'James')
    yield ('1PET', 5, '1 Peter')
    yield ('2PET', 3, '2 Peter')
    yield ('1JOHN', 5, '1 John')
    yield ('2JOHN', 1, '2 John')
    yield ('3JOHN', 1, '3 John')
    yield ('JUDE', 1, 'Jude')

    yield ('REV', 22, 'Revelation')


class BibleChapter:
    def __init__(self, code_name: str, chapter: int, full_name: str):
        self.code_name, self.chapter, self.full_name = code_name, chapter, full_name

        file_path = 'html/%s+%d.html' % (self.code_name, self.chapter)
        with open(file_path, 'r') as file:
            self.html = file.read()


def yield_chapters():
    for (code_name, chapter_count, full_name) in yield_books():
        for chapter in range(1, chapter_count + 1):
            ch = BibleChapter(code_name, chapter, full_name)
            yield ch


