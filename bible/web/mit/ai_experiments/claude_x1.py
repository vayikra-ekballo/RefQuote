#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
import re

def parse_psalm_html(html_content):
    """
    Parse HTML content of Psalm 23 and convert it to a structured JSON format.
    """
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title = soup.title.text if soup.title else "Unknown Title"
    
    # Find the Psalm heading (B tag before DL)
    psalm_heading = soup.find('b').text if soup.find('b') else "Unknown Psalm"
    
    # Extract the psalm description (first DD text)
    description = soup.find('dl').find('dd').text if soup.find('dl') and soup.find('dl').find('dd') else ""
    
    # Extract verses
    dl_tag = soup.find('dl', {'compact': True})
    verses = []
    
    if dl_tag:
        dt_tags = dl_tag.find_all('dt')
        dd_tags = dl_tag.find_all('dd')
        
        # Start from the second verse (index 1) as the first is the description
        for i in range(1, len(dt_tags)):
            if i < len(dd_tags):
                verse_num = dt_tags[i].text.strip()
                verse_text = dd_tags[i].text.strip()
                
                # Clean up verse text by removing footnote references
                verse_text = re.sub(r'\[\d+\]', '', verse_text)
                verse_text = re.sub(r'\s+', ' ', verse_text).strip()
                
                verses.append({
                    "number": verse_num,
                    "text": verse_text
                })
    
    # Extract footnotes
    footnotes = []
    footnote_ol = soup.find('ol')
    if footnote_ol and footnote_ol.find_all('li'):
        for li in footnote_ol.find_all('li'):
            footnote_text = li.text.strip()
            # Extract footnote number and text
            footnote_match = re.match(r'\[(\d+)\](.*)', footnote_text)
            if footnote_match:
                footnote_num = footnote_match.group(1)
                footnote_content = footnote_match.group(2).strip()
                footnotes.append({
                    "number": footnote_num,
                    "text": footnote_content
                })
    
    # Construct the final JSON structure
    psalm_json = {
        "title": title,
        "psalm": psalm_heading,
        "description": description,
        "verses": verses,
        "footnotes": footnotes
    }
    
    return psalm_json

def main():
    # The HTML content provided in the prompt
    html_content = """<HTML> <HEAD> <TITLE>Bible Gateway Psalm 23 :: NIV</TITLE> <link href="ss.css" tppabs="http://www.ugcs.caltech.edu/~werdna/nnh/bibles/niv/ss.css" rel="stylesheet" type="text/css"> </HEAD> <BODY BGCOLOR="#ffffcc"> </DL><B>Psalm 23</B><DL COMPACT><DT>1 <DD>Psalm 23 A psalm of David.<DT>1 <DD>The LORD is my shepherd, I shall not be in want.<DT>2 <DD>He makes me lie down in green pastures, he leads me beside quiet waters,<DT>3 <DD>he restores my soul. He guides me in paths of righteousness for his name's sake.<DT>4 <DD>Even though I walk through the valley of the shadow of death, <sup>[<a href="#footnote_252747245_1">1</a>]</sup> I will fear no evil, for you are with me; your rod and your staff, they comfort me. <DT>5 <DD>You prepare a table before me in the presence of my enemies. You anoint my head with oil; my cup overflows.<DT>6 <DD>Surely goodness and love will follow me all the days of my life, and I will dwell in the house of the LORD forever. </DL><OL><LI><A NAME="footnote_252747245_1">[4] Or <I>through the darkest valley</I></A></LI> </OL> <OL></OL> <BR> <BR> </TR> </BODY> </HTML>"""
    
    # Parse the HTML and convert to JSON
    psalm_json = parse_psalm_html(html_content)
    
    # Print the JSON with nice formatting
    print(json.dumps(psalm_json, indent=2))
    
    # Optionally save to a file
    with open('psalm_23.json', 'w') as f:
        json.dump(psalm_json, f, indent=2)
    
    print("JSON has been saved to 'psalm_23.json'")

if __name__ == "__main__":
    main()

