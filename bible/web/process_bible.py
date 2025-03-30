#!/usr/bin/env python3

import re
import json
from bs4 import BeautifulSoup
from yield_books import yield_protestant_canon_books


class BibleChapter:
	def __init__(self, verses_with_num, title, subtitle):
		self.title = title
		self.subtitle = subtitle

		# Assert that verse numbers are 1 to N
		for i, verse in enumerate(verses_with_num):
			assert verse['number'] == str(i + 1)
		# Transform verses into a list of strings
		verses = [verse['text'] for verse in verses_with_num]

		self.verses = verses

	@staticmethod
	def scrub(text, clean=False):
		# Remove footnote markers like [a] and cross-reference markers like (A) and superscript references
		return (re.sub(r'\[\w+\]|\(\w+\)', '', text)).strip()

	def display(self, clean=False):
		title = self.scrub(self.title) if clean else self.title
		if self.subtitle is not None:
			subtitle = self.scrub(self.subtitle) if clean else self.subtitle
		verses = [self.scrub(verse) for verse in self.verses] if clean else self.verses
		print(f'Title: {title}')
		if self.subtitle is not None:
			print(f'Subtitle: {subtitle}')
		print('Verses:')
		for i in range(len(verses)):
			print(f'  {i + 1}: {verses[i]}')

	def get_simple_dict(self):
		d = {'title': self.title, 'verses': self.verses}
		if self.subtitle is not None:
			d['subtitle'] = self.subtitle
		return d


def process_chapter(html):
	soup = BeautifulSoup(html, 'html.parser')

	title = soup.find('span', class_='text').text.strip()
	subtitle_h4 = soup.find('h4')
	subtitle = subtitle_h4.find('span', class_='text').text.strip() if subtitle_h4 else None
	verses_with_num = []

	# Process each verse
	current_verse = None
	verse_number = None
	for span in soup.find_all('span', class_=lambda c: c and c.startswith('text')):
		# Check if this span contains a verse number
		verse_num_sup = span.find('sup', class_='versenum')

		if verse_num_sup:
			# If we have a previous verse, add it to our collection
			if current_verse is not None and verse_number is not None:
				verses_with_num.append({'number': verse_number, 'text': current_verse.strip()})

			# Start a new verse
			verse_number = verse_num_sup.text.strip()
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

	return BibleChapter(verses_with_num, title, subtitle)


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
	verses_html = bible_html['Jude'][1 - 1]['verses_html']
	r = process_chapter(verses_html)
	r.display(True)


if __name__ == '__main__':
	process_bible('NET')
