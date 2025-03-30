#!/usr/bin/env python3

import re
import json
from bs4 import BeautifulSoup
from yield_books import yield_protestant_canon_books


def process_2(html_content):
	soup = BeautifulSoup(html_content, 'html.parser')

	# Extract the title and subtitle
	title = soup.find('span', class_='text Ps-23-1', id='en-NIV-14237').text.strip()
	subtitle = soup.find('h4').find('span', class_='text Ps-23-1').text.strip()

	# Initialize the structure
	psalm_json = {'title': title, 'subtitle': subtitle, 'verses': []}

	# Find all verse numbers
	verse_spans = soup.find_all(
		'span',
		class_=lambda c: c
		and c.startswith('text Ps-23-')
		and 'versenum' in [s.get('class', [''])[0] for s in soup.find_all('sup') if s.parent == c],
	)

	# Process each verse
	current_verse = None
	verse_number = None

	for span in soup.find_all('span', class_=lambda c: c and c.startswith('text Ps-23-')):
		# Check if this span contains a verse number
		verse_num_sup = span.find('sup', class_='versenum')

		if verse_num_sup:
			# If we have a previous verse, add it to our collection
			if current_verse is not None and verse_number is not None:
				psalm_json['verses'].append({'number': verse_number, 'text': current_verse.strip()})

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
		psalm_json['verses'].append({'number': verse_number, 'text': current_verse.strip()})

	# Assert that verse numbers are 1 to N
	for i, verse in enumerate(psalm_json['verses']):
		assert verse['number'] == str(i + 1)
	# Transform verses into a list of strings
	psalm_json['verses'] = [verse['text'] for verse in psalm_json['verses']]

	# Clean up the verses by removing footnote references and cross-references
	for i in range(len(psalm_json['verses'])):
		# Remove footnote markers like [a] and cross-reference markers like (A)
		text = psalm_json['verses'][i]
		# Remove superscript references
		text = re.sub(r'\[\w\]|\(\w\)', '', text)
		psalm_json['verses'][i] = text.strip()

	return psalm_json


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
	verses_html = bible_html['Psalms'][23 - 1]['verses_html']
	r = process_2(verses_html)
	print(json.dumps(r, indent=4))


if __name__ == '__main__':
	process_bible('NIV')
