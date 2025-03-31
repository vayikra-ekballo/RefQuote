#!/usr/bin/env python3

import re
import json
from tqdm import tqdm
from typing import Optional
from bs4 import BeautifulSoup
from multiprocessing import Pool
from dataclasses import dataclass
from yield_books import yield_protestant_canon_books


class BibleChapter:
	@dataclass
	class Section:
		heading: str
		verses: list[int]

		def as_dict(self):
			return {'heading': self.heading, 'verses': self.verses}

	@dataclass
	class VerseWithNum:
		number: int
		text: str

	def __init__(
		self,
		book_name: str,
		chapter: int,
		verses_with_num: list[VerseWithNum],
		sections: list[Section],
		woj: list[int],
		title: str,
		subtitle: str,
	):
		self.book_name = book_name
		self.chapter = chapter
		self.sections = sections
		self.woj = woj
		self.title = title
		self.subtitle = subtitle

		# Assert that verse numbers are 1 to N
		for i, verse in enumerate(verses_with_num):
			if str(verse.number) != str(i + 1):
				raise Exception(f'Unexpected verse number: {repr(verse.number)} -- expected {repr(i + 1)}')
		# Transform verses into a list of strings
		verses = [verse.text for verse in verses_with_num]

		self.verses = verses

	@staticmethod
	def scrub(text, clean=False):
		# Remove footnote markers like [a] and cross-reference markers like (A) and superscript references
		return (re.sub(r'\[\w+\]|\(\w+\)', '', text)).strip()

	def display(self, clean=False):
		d = self.get_simple_dict(clean)
		p = f'Title: {d["title"]}\n'
		if 'subtitle' in d:
			p += f'Subtitle: {d["subtitle"]}\n'
		p += 'Verses:\n'
		for i in range(len(d['verses'])):
			verse_num = i + 1
			if verse_num in d['headings']:
				p += f'[Heading: {d["headings"][verse_num]}:]\n'
			p += f'  {verse_num}: {d["verses"][i]}\n'
		if len(self.woj) > 0:
			p += f'Words of Jesus: {self.woj}\n'
		print(p)

	@staticmethod
	def get_headings(sections: list[Section]):
		return {(section.verses[0] if len(section.verses) > 0 else None): section.heading for section in sections}

	def get_simple_dict(self, clean=False):
		title = self.scrub(self.title) if clean else self.title
		verses = [self.scrub(verse) for verse in self.verses] if clean else self.verses
		sections = [BibleChapter.Section(self.scrub(section.heading), section.verses) for section in self.sections]
		headings = self.get_headings(sections)
		d = {'title': title, 'verses': verses, 'woj': self.woj, 'sections': sections, 'headings': headings}
		if self.subtitle is not None:
			subtitle = self.scrub(self.subtitle) if clean else self.subtitle
			d['subtitle'] = subtitle
		return d

	@staticmethod
	def extract_verse_num(verse_num_elem) -> Optional[int]:
		try:
			return int(verse_num_elem.text.strip()) if verse_num_elem else None
		except ValueError:
			verse_num_text = verse_num_elem.text.strip()
			if verse_num_text[0] == '[' and verse_num_text[-1] == ']':
				verse_num_text = verse_num_text[1:-1]
				return int(verse_num_text)
			else:
				raise Exception(f'Unexpected verse number: {verse_num_text}')

	@staticmethod
	def process(raw_chapter: 'RawBibleChapter') -> 'BibleChapter':
		verses_html = raw_chapter.verses_html
		soup = BeautifulSoup(verses_html, 'html.parser')

		title = soup.find('span', class_='text').text.strip()
		subtitle_h4 = soup.find('h4')
		subtitle = subtitle_h4.find('span', class_='text').text.strip() if subtitle_h4 else None
		verses_with_num = []

		# Find all section headers (h3 tags)
		sections = []
		woj_verses = []
		section_headers = soup.find_all('h3')
		for header in section_headers:
			# Create a new section
			section = BibleChapter.Section(heading=header.text.strip(), verses=[])

			# Find all the paragraph elements following this header until the next header
			next_element = header.next_sibling

			while next_element and (not isinstance(next_element, type(header)) or next_element.name != 'h3'):
				if hasattr(next_element, 'name') and next_element.name in ['p', 'div']:
					# Process paragraphs or divs containing verses
					verse_spans = next_element.find_all('span', class_=lambda c: c and c.startswith('text'))

					for span in verse_spans:
						# Extract verse number
						verse_num_elem = span.find('sup', class_='versenum')
						chapter_num_span = span.find('span', class_='chapternum')
						verse_num = BibleChapter.extract_verse_num(verse_num_elem)
						if chapter_num_span:
							verse_num = 1

						if verse_num:
							# Check if this span has "words of Jesus" spans
							woj_spans = span.find_all('span', class_='woj')

							if woj_spans:
								# This is words of Jesus
								woj_verses.append(verse_num)

							# Add to verses list
							section.verses.append(verse_num)

				next_element = next_element.next_sibling

			# Add the section to the result
			sections.append(section)

		for h3elem in soup.find_all('h3'):
			h3elem.extract()

		# Process each verse
		current_verse = None
		verse_number = None
		for span in soup.find_all('span', class_=lambda c: c and c.startswith('text')):
			# Check if this span contains a chapter number
			chapter_num_span = span.find('span', class_='chapternum')
			# Check if this span contains a verse number
			verse_num_sup = span.find('sup', class_='versenum')

			if chapter_num_span:
				# If we have a previous verse, add it to our collection
				if current_verse is not None or verse_number is not None:
					raise Exception('Unexpected chapter number')

				# Start a new chapter
				verse_number = 1
				# Remove the chapter number from the text
				verse_text = span.text.replace(chapter_num_span.text, '', 1).strip()
				current_verse = verse_text
			elif verse_num_sup:
				# If we have a previous verse, add it to our collection
				if current_verse is not None and verse_number is not None:
					verses_with_num.append(BibleChapter.VerseWithNum(verse_number, current_verse.strip()))

				# Start a new verse
				verse_number = BibleChapter.extract_verse_num(verse_num_sup)
				# Remove the verse number from the text
				verse_text = span.text.replace(verse_num_sup.text, '', 1).strip()
				current_verse = verse_text
			else:
				# This is a continuation of the current verse
				if current_verse is not None:
					# Add this text to the current verse
					current_verse += ' ' + span.text.strip()

		# Don't forget to add the last verse
		if current_verse is not None and verse_number is not None:
			verses_with_num.append(BibleChapter.VerseWithNum(verse_number, current_verse.strip()))

		return BibleChapter(
			raw_chapter.book_name, raw_chapter.chapter, verses_with_num, sections, woj_verses, title, subtitle
		)

	def get_json(self):
		chapter_json = {'title': self.title, 'verses': self.verses}
		if len(self.sections) > 0:
			chapter_json['headings'] = self.get_headings(self.sections)
		if len(self.woj) > 0:
			chapter_json['woj'] = self.woj
		if self.subtitle is not None:
			chapter_json['subtitle'] = self.subtitle
		return chapter_json


@dataclass
class RawBibleChapter:
	book_name: str
	chapter: int
	verses_html: str
	footnotes_html: str
	crossrefs_html: Optional[str]


def grab_bible_html(translation: str) -> dict:
	bible_html = {}

	def get_file_name(translation: str, book_name: str) -> str:
		return f'archive/{translation.lower()}/{book_name}.html.json'

	for book_name, _ in yield_protestant_canon_books():
		file_name = get_file_name(translation, book_name)
		with open(file_name, 'r') as f:
			book = json.load(f)
		bible_html[book_name] = book
	return bible_html


def process_chapter(raw_chapter: RawBibleChapter) -> BibleChapter:
	# print(f'Processing {raw_chapter.book_name} {raw_chapter.chapter}...', end='\r')
	return BibleChapter.process(raw_chapter)


def process_bible(translation: str):
	print(f'Processing {translation}...')
	translation = translation.lower()
	bible_html = grab_bible_html(translation)

	raw_chapters: list[RawBibleChapter] = []
	for book_name, chapter_count in yield_protestant_canon_books():
		for i in range(chapter_count):
			verses_html = bible_html[book_name][i]['verses_html']
			footnotes_html = bible_html[book_name][i]['footnotes_html']
			crossrefs_html = None
			if 'crossrefs_html' in bible_html[book_name][i]:
				crossrefs_html = bible_html[book_name][i]['crossrefs_html']
			raw_chapters.append(
				RawBibleChapter(
					book_name,
					i + 1,
					verses_html,
					footnotes_html,
					crossrefs_html,
				)
			)

	with Pool() as p:
		chapters: list[BibleChapter] = list(tqdm(p.imap(process_chapter, raw_chapters, chunksize=10), total=1189))

	bible = {'books': {}}

	for full_name, chapter_count in yield_protestant_canon_books():
		for chapter_json in range(1, chapter_count + 1):
			if full_name not in bible['books']:
				bible['books'][full_name] = []
			bible['books'][full_name].append(None)

	for chapter in chapters:
		bible['books'][chapter.book_name][chapter.chapter - 1] = chapter.get_json()

	output_json_path = f'../json/{translation}.json'
	with open(output_json_path, 'w') as f:
		json.dump(bible, f, indent='\t', ensure_ascii=False)
	print('Done. Written to: %s' % output_json_path)


if __name__ == '__main__':
	process_bible('NIV')
	# process_bible('NLT')
	# process_bible('ESV')
	# process_bible('NET')
