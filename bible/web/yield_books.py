from typing import Generator


def yield_protestant_canon_books() -> Generator[tuple[str, int]]:
    """Yield tuples with book name & chapter count."""

    # The Old Testament
    # -----------------

    # Torah
    yield "Genesis", 50
    yield "Exodus", 40
    yield "Leviticus", 27
    yield "Numbers", 36
    yield "Deuteronomy", 34

    # Historical Books
    yield "Joshua", 24
    yield "Judges", 21
    yield "Ruth", 4
    yield "1 Samuel", 31
    yield "2 Samuel", 24
    yield "1 Kings", 22
    yield "2 Kings", 25
    yield "1 Chronicles", 29
    yield "2 Chronicles", 36
    yield "Ezra", 10
    yield "Nehemiah", 13
    yield "Esther", 10

    # Poetic Books
    yield "Job", 42
    yield "Psalms", 150
    yield "Proverbs", 31
    yield "Ecclesiastes", 12
    yield "Song of Songs", 8

    # Major Prophets
    yield "Isaiah", 66
    yield "Jeremiah", 52
    yield "Lamentations", 5
    yield "Ezekiel", 48
    yield "Daniel", 12

    # Minor Prophets
    yield "Hosea", 14
    yield "Joel", 3
    yield "Amos", 9
    yield "Obadiah", 1
    yield "Jonah", 4
    yield "Micah", 7
    yield "Nahum", 3
    yield "Habakkuk", 3
    yield "Zephaniah", 3
    yield "Haggai", 2
    yield "Zechariah", 14
    yield "Malachi", 4

    # The New Testament
    # -----------------

    # The Gospels & Acts
    yield "Matthew", 28
    yield "Mark", 16
    yield "Luke", 24
    yield "John", 21
    yield "Acts", 28

    # Letters of Paul & others
    yield "Romans", 16
    yield "1 Corinthians", 16
    yield "2 Corinthians", 13
    yield "Galatians", 6
    yield "Ephesians", 6
    yield "Philippians", 4
    yield "Colossians", 4
    yield "1 Thessalonians", 5
    yield "2 Thessalonians", 3
    yield "1 Timothy", 6
    yield "2 Timothy", 4
    yield "Titus", 3
    yield "Philemon", 1
    yield "Hebrews", 13

    # Letters of James, Peter & John
    yield "James", 5
    yield "1 Peter", 5
    yield "2 Peter", 3
    yield "1 John", 5
    yield "2 John", 1
    yield "3 John", 1

    # Final
    yield "Jude", 1
    yield "Revelation", 22
