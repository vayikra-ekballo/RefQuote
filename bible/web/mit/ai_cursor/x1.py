#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re


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
        raise Exception("Unknown Title")

    # Extract just the verses
    m = re.search(r'<DL COMPACT>.*?', verses_plus_title_html, re.DOTALL)
    s = m.start() + len('<DL COMPACT>')
    verses_html = verses_plus_title_html[s:].strip()

    return {
        'title': title,
        'verses_html': verses_html,
        'footnotes_html': footnotes_html
    }


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


def verses_html_iterator(html):
    # print(html)

    # Use regex to find all verse sections (DT and DD pairs)
    pattern = r'<DT>(\d+)\s*<DD>(.*?)(?=<DT>|$)'
    matches = re.findall(pattern, html, re.DOTALL)
    
    # Process each match to clean HTML and create structured data
    for number, content in matches:
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract text and remove unnecessary whitespace
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text).strip()
        
        yield (int(number), text)


def process_verses(html):
    verses = dict()
    subheading = None

    for (vn, verse) in verses_html_iterator(html):
        if vn not in verses:
            verses[vn] = verse
        else:
            if vn == 1:
                subheading = verses[1]
                verses[1] = verse
            else:
                raise Exception('Repeating verse: %d.' % vn)

    verses_array = []
    for i in range(1, len(verses) + 1):
        verses_array.append(verses[i])

    return (subheading, verses_array)


def process_html(html):
    portions = extract_html_portions(html)
    title = portions['title']
    footnotes = footnotes_html_to_array(portions['footnotes_html'])
    subheading, verses = process_verses(portions['verses_html'])

    print('Title:', title, '\n')
    print('Subheading:', subheading, '\n')
    print('Verses:', verses, '\n')
    print('Footnotes:', footnotes, '\n')


def get_test_file():
    with open('../html/PS+24.html', 'r') as file:
        return file.read()


def main():
    html = get_test_file()
    process_html(html)


if __name__ == "__main__":
    main()
