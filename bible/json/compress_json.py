#!/usr/bin/env python3

import re
import json
from collections import defaultdict

def find_repeating_substrings(strings):
    """Finds all repeating substrings across the list of strings."""
    substring_map = defaultdict(int)  # Tracks occurrences
    repeating_substrings = set()

    for s in strings:
        seen_in_current = set()  # Track substrings in the current string
        length = len(s)
        
        for i in range(length):
            for j in range(i + 1, length + 1):
                substring = s[i:j]
                if substring in seen_in_current:
                    repeating_substrings.add(substring)
                else:
                    substring_map[substring] += 1
                    if substring_map[substring] > 1:
                        repeating_substrings.add(substring)
                    seen_in_current.add(substring)

    return sorted(repeating_substrings, key=len, reverse=True)  # Sort longest first

def replace_with_numbers(strings):
    """Replaces repeating substrings with numbered placeholders."""
    repeating_substrings = find_repeating_substrings(strings)
    substring_to_number = {sub: f"{{{i}}}" for i, sub in enumerate(repeating_substrings)}
    
    def regex_replace(s, substring_map):
        """Replaces substrings using regex word boundaries for precision."""
        # Use a compiled regex to replace all substrings efficiently
        regex = re.compile("|".join(map(re.escape, substring_map.keys())))
        return regex.sub(lambda match: substring_map[match.group(0)], s)

    compressed_strings = [regex_replace(s, substring_to_number) for s in strings]

    return compressed_strings, substring_to_number

# # Example usage
# strings = ["banana", "anaban", "nabanan"]
# compressed, mapping = replace_with_numbers(strings)

# print("Compressed Strings:")
# for s in compressed:
#     print(s)

# print("\nSubstring Mapping:")
# for k, v in mapping.items():
#     print(f"{v}: {k}")

with open('mit.json', 'r') as f:
	bible = json.loads(f.read())

verses = []

for book_name, book in bible['books'].items():
	for ch in book:
		verses.extend(ch['verses'])


print(len(verses))
compressed, mapping = replace_with_numbers(verses)

