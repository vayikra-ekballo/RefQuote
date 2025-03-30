#!/usr/bin/env python3

import re
import json
from bs4 import BeautifulSoup
from yield_books import yield_protestant_canon_books


class BibleChapter:
	def __init__(self, verses_with_num, sections, woj, title, subtitle):
		self.sections = sections
		self.headings = {section['verses'][0]: section['heading'] for section in sections}
		self.woj = woj
		self.title = title
		self.subtitle = subtitle

		# Assert that verse numbers are 1 to N
		for i, verse in enumerate(verses_with_num):
			if str(verse['number']) != str(i + 1):
				raise Exception(f'Unexpected verse number: {repr(verse["number"])} -- expected {repr(i + 1)}')
		# Transform verses into a list of strings
		verses = [verse['text'] for verse in verses_with_num]

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
			if verse_num in self.headings:
				p += f'[Heading: {self.headings[verse_num]}:]\n'
			p += f'  {verse_num}: {d["verses"][i]}\n'
		if len(self.woj) > 0:
			p += f'Words of Jesus: {self.woj}\n'
		print(p)

	def get_simple_dict(self, clean=False):
		title = self.scrub(self.title) if clean else self.title
		verses = [self.scrub(verse) for verse in self.verses] if clean else self.verses
		d = {'title': title, 'verses': verses}
		if self.subtitle is not None:
			subtitle = self.scrub(self.subtitle) if clean else self.subtitle
			d['subtitle'] = subtitle
		return d

	@staticmethod
	def process_chapter(html):
		soup = BeautifulSoup(html, 'html.parser')

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
			section = {'heading': header.text.strip(), 'verses': []}

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
						verse_num = int(verse_num_elem.text.strip()) if verse_num_elem else None
						if chapter_num_span:
							verse_num = 1

						if verse_num:
							# Check if this span has "words of Jesus" spans
							woj_spans = span.find_all('span', class_='woj')

							if woj_spans:
								# This is words of Jesus
								woj_verses.append(verse_num)

							# Add to verses list
							section['verses'].append(verse_num)

				next_element = next_element.next_sibling

			# Add the section to the result
			sections.append(section)

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
					verses_with_num.append({'number': verse_number, 'text': current_verse.strip()})

				# Start a new verse
				verse_number = int(verse_num_sup.text.strip())
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
			verses_with_num.append({'number': verse_number, 'text': current_verse.strip()})

		return BibleChapter(verses_with_num, sections, woj_verses, title, subtitle)


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


def process_bible(translation: str):
	bible_html = grab_bible_html(translation)
	# verses_html = bible_html['Psalms'][23 - 1]['verses_html']
	# verses_html = bible_html['Psalms'][117 - 1]['verses_html']
	verses_html = bible_html['Matthew'][5 - 1]['verses_html']
	# verses_html = bible_html['Jude'][1 - 1]['verses_html']
	r = BibleChapter.process_chapter(verses_html)
	r.display(True)


if __name__ == '__main__':
	process_bible('NIV')
