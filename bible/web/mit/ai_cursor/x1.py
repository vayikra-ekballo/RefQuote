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


def verses_html_to_array(html):
    print(html)


def get_test_file():
    with open('../html/PS+24.html', 'r') as file:
        return file.read()


def main():
    html_content = get_test_file()
    portions = extract_html_portions(html_content)
    footnotes = footnotes_html_to_array(portions['footnotes_html'])
    print('Title:', portions['title'], '\n')
    print('Footnotes:', footnotes, '\n')
    verses_html_to_array(portions['verses_html'])


if __name__ == "__main__":
    main()
