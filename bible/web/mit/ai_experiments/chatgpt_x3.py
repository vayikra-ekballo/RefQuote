#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json

def parse_html_to_json(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract title
    title = soup.title.string if soup.title else ""
    
    # Extract Psalm 23 text
    psalm = {"title": title, "verses": {}}
    
    for dt, dd in zip(soup.find_all('dt'), soup.find_all('dd')):
        verse_number = dt.get_text(strip=True)
        if verse_number.isdigit():
            verse_number = int(verse_number)
        verse_text = dd.get_text(" ", strip=True)
        psalm["verses"][verse_number] = verse_text
    
    # Extract footnotes
    footnotes = []
    for li in soup.find_all('li'):
        footnote_text = li.get_text(strip=True)
        footnotes.append(footnote_text)
    
    if footnotes:
        psalm["footnotes"] = footnotes
    
    return json.dumps(psalm, indent=4)

# Sample HTML input
html_input = """<HTML>
<HEAD>
<TITLE>Bible Gateway Psalm 23 :: NIV</TITLE>
<link href="ss.css" tppabs="http://www.ugcs.caltech.edu/~werdna/nnh/bibles/niv/ss.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY BGCOLOR="#ffffcc">
</DL><B>Psalm 23</B><DL COMPACT><DT>1 <DD>Psalm 23  A psalm of David.<DT>1 <DD>The LORD is my shepherd, I shall not be in want.<DT>2 <DD>He makes me lie down in green pastures, he leads me beside quiet waters,<DT>3 <DD>he restores my soul. He guides me in paths of righteousness for his name's sake.<DT>4 <DD>Even though I walk through the valley of the shadow of death, <sup>[<a href="#footnote_252747245_1">1</a>]</sup>   I will fear no evil, for you are with me; your rod and your staff, they comfort me. <DT>5 <DD>You prepare a table before me in the presence of my enemies. You anoint my head with oil; my cup overflows.<DT>6 <DD>Surely goodness and love will follow me all the days of my life, and I will dwell in the house of the LORD forever. </DL><OL><LI><A NAME="footnote_252747245_1">[4] Or <I>through the darkest valley</I></A></LI>
</OL>
</OL>
<BR>
<BR>
</TR>

</BODY>
</HTML>"""

# Convert to JSON
json_output = parse_html_to_json(html_input)
print(json_output)
