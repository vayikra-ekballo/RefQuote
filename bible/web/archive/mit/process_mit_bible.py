#!/usr/bin/env python3

from collections import OrderedDict
from multiprocessing import Pool
from bs4 import BeautifulSoup
import json
import re


def yield_books():
	# Old Testament:

	yield 'GEN', 50, 'Genesis'
	yield 'EXOD', 40, 'Exodus'
	yield 'LEV', 27, 'Leviticus'
	yield 'NUM', 36, 'Numbers'
	yield 'DEUT', 34, 'Deuteronomy'

	yield 'JOSH', 24, 'Joshua'
	yield 'JUDG', 21, 'Judges'
	yield 'RUTH', 4, 'Ruth'

	yield '1SAM', 31, '1 Samuel'
	yield '2SAM', 24, '2 Samuel'

	yield '1KGS', 22, '1 Kings'
	yield '2KGS', 25, '2 Kings'

	yield '1CHRON', 29, '1 Chronicles'
	yield '2CHRON', 36, '2 Chronicles'

	yield 'EZRA', 10, 'Ezra'
	yield 'NEH', 13, 'Nehemiah'
	yield 'ESTH', 10, 'Esther'
	yield 'JOB', 42, 'Job'

	yield 'PS', 150, 'Psalms'

	yield 'PROV', 31, 'Proverbs'
	yield 'ECC', 12, 'Ecclesiastes'

	yield 'SONG', 8, 'Song of Songs'

	yield 'ISA', 66, 'Isaiah'
	yield 'JER', 52, 'Jeremiah'

	yield 'LAM', 5, 'Lamentations'

	yield 'EZEK', 48, 'Ezekiel'
	yield 'DAN', 12, 'Daniel'

	yield 'HOSEA', 14, 'Hosea'
	yield 'JOEL', 3, 'Joel'
	yield 'AMOS', 9, 'Amos'
	yield 'OBAD', 1, 'Obadiah'
	yield 'JONAH', 4, 'Jonah'
	yield 'MICAH', 7, 'Micah'
	yield 'NAHUM', 3, 'Nahum'
	yield 'HAB', 3, 'Habakkuk'
	yield 'ZEPH', 3, 'Zephaniah'
	yield 'HAG', 2, 'Haggai'
	yield 'ZECH', 14, 'Zechariah'
	yield 'MAL', 4, 'Malachi'

	# New Testament:

	yield 'MATT', 28, 'Matthew'
	yield 'MARK', 16, 'Mark'
	yield 'LUKE', 24, 'Luke'
	yield 'JOHN', 21, 'John'

	yield 'ACTS', 28, 'Acts'
	yield 'ROM', 16, 'Romans'

	yield '1COR', 16, '1 Corinthians'
	yield '2COR', 13, '2 Corinthians'

	yield 'GAL', 6, 'Galatians'
	yield 'EPH', 6, 'Ephesians'
	yield 'PHIL', 4, 'Philippians'
	yield 'COL', 4, 'Colossians'

	yield '1THES', 5, '1 Thessalonians'
	yield '2THES', 3, '2 Thessalonians'

	yield '1TIM', 6, '1 Timothy'
	yield '2TIM', 4, '2 Timothy'

	yield 'TIT', 3, 'Titus'
	yield 'PHILEM', 1, 'Philemon'

	yield 'HEB', 13, 'Hebrews'
	yield 'JAS', 5, 'James'
	yield '1PET', 5, '1 Peter'
	yield '2PET', 3, '2 Peter'
	yield '1JOHN', 5, '1 John'
	yield '2JOHN', 1, '2 John'
	yield '3JOHN', 1, '3 John'
	yield 'JUDE', 1, 'Jude'

	yield 'REV', 22, 'Revelation'


class RawBibleChapter:
	def __init__(self, code_name: str, chapter: int, full_name: str):
		self.code_name, self.chapter, self.full_name = code_name, chapter, full_name

		file_path = 'html/%s+%d.html' % (self.code_name, self.chapter)
		with open(file_path, 'r') as file:
			self.html = file.read()


def yield_chapters():
	for code_name, chapter_count, full_name in yield_books():
		for chapter in range(1, chapter_count + 1):
			ch = RawBibleChapter(code_name, chapter, full_name)
			yield ch


class BibleChapter(RawBibleChapter):
	def __init__(self, ch: RawBibleChapter, log=False):
		super().__init__(ch.code_name, ch.chapter, ch.full_name)
		if log == True:
			print('Processing %s %d...' % (ch.full_name, ch.chapter))

		portions = self.extract_html_portions(ch.html)
		self.title = portions['title']
		self.footnotes = self.footnotes_html_to_array(portions['footnotes_html'])
		self.subheading, self.verses, self.skipped_verse_numbers = self.process_verses(portions['verses_html'])

	def display(self):
		print('Title:', self.title, '\n')
		print('Subheading:', self.subheading, '\n')
		print('Verses:', self.verses, '\n')
		if len(self.skipped_verse_numbers) > 0:
			print('Skipped verses:', self.skipped_verse_numbers)
		print('Footnotes:', self.footnotes, '\n')

	def process_verses(self, html):
		verses = dict()
		subheading = None

		for vn, verse in self.verses_html_iterator(html):
			if vn not in verses:
				verses[vn] = verse
			else:
				if vn == 1:
					subheading = verses[1]
					if subheading.startswith(self.title):
						subheading = subheading[len(self.title) :].strip()
						if len(subheading) == 0:
							subheading = None
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

	@staticmethod
	def verses_html_iterator(html):
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

	@staticmethod
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

	@staticmethod
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
			raise Exception('Unknown Title')

		# Extract just the verses
		m = re.search(r'<DL COMPACT>.*?', verses_plus_title_html, re.DOTALL)
		s = m.start() + len('<DL COMPACT>')
		verses_html = verses_plus_title_html[s:].strip()

		return {
			'title': title,
			'verses_html': verses_html,
			'footnotes_html': footnotes_html,
		}


def process_chapter(raw_chapter: RawBibleChapter) -> BibleChapter:
	return BibleChapter(raw_chapter)


def process_bible():
	raw_chapters = list(yield_chapters())

	total_chapters_count = len(raw_chapters)
	assert total_chapters_count == 1189

	with Pool() as p:
		chapters = p.map(process_chapter, raw_chapters)

	bible = {'books': OrderedDict()}

	for code_name, chapter_count, full_name in yield_books():
		for chapter in range(1, chapter_count + 1):
			if full_name not in bible['books']:
				bible['books'][full_name] = []
			bible['books'][full_name].append(None)

	for ch in chapters:
		chapter = OrderedDict()
		chapter['title'] = ch.title
		if ch.subheading is not None:
			chapter['subheading'] = ch.subheading
		chapter['verses'] = ch.verses
		if len(ch.skipped_verse_numbers) > 0:
			chapter['skippedVerseNumbers'] = ch.skipped_verse_numbers
		chapter['footnotes'] = ch.footnotes

		bible['books'][ch.full_name][ch.chapter - 1] = chapter

	bible_json = json.dumps(bible, indent='\t')
	output_json_path = '../../../json/mit.json'
	with open(output_json_path, 'w') as f:
		f.write(bible_json)

	print('Done. Written to: %s' % output_json_path)


if __name__ == '__main__':
	process_bible()
