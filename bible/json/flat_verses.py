#!/usr/bin/env python3

import json

with open('mit.json', 'r') as f:
	bible = json.loads(f.read())

verses = []

for book_name, book in bible['books'].items():
	for ch in book:
		verses.extend(ch['verses'])

with open('mit_verses_flat.txt', 'w') as f:
	for v in verses:
		f.write(v + '\n')

