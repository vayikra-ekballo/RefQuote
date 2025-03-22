#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json, re, sys

# html_content0 = """
# <HTML>
# <HEAD>
# <TITLE>Bible Gateway Psalm 23 :: NIV</TITLE>
# <link href="ss.css" tppabs="http://www.ugcs.caltech.edu/~werdna/nnh/bibles/niv/ss.css" rel="stylesheet" type="text/css">
# </HEAD>
# <BODY BGCOLOR="#ffffcc">
# </DL><B>Psalm 23</B><DL COMPACT>
# <DT>1 <DD>Psalm 23  A psalm of David.
# <DT>1 <DD>The LORD is my shepherd, I shall not be in want.
# <DT>2 <DD>He makes me lie down in green pastures, he leads me beside quiet waters,
# <DT>3 <DD>he restores my soul. He guides me in paths of righteousness for his name's sake.
# <DT>4 <DD>Even though I walk through the valley of the shadow of death, <sup>[<a href="#footnote_252747245_1">1</a>]</sup> I will fear no evil, for you are with me; your rod and your staff, they comfort me.
# <DT>5 <DD>You prepare a table before me in the presence of my enemies. You anoint my head with oil; my cup overflows.
# <DT>6 <DD>Surely goodness and love will follow me all the days of my life, and I will dwell in the house of the LORD forever.
# </DL>
# <OL>
#     <LI><A NAME="footnote_252747245_1">[4] Or <I>through the darkest valley</I></A></LI>
# </OL>
# </BODY>
# </HTML>
# """

html_content = """
<HTML>
<HEAD>
<TITLE>Bible Gateway Psalm 24 :: NIV</TITLE>
<link href="ss.css" tppabs="http://www.ugcs.caltech.edu/~werdna/nnh/bibles/niv/ss.css" rel="stylesheet" type="text/css">
</HEAD>
<BODY BGCOLOR="#ffffcc">
</DL><B>Psalm 24</B><DL COMPACT><DT>1 <DD>Psalm 24  Of David. A psalm.<DT>1 <DD>The earth is the LORD's, and everything in it, the world, and all who live in it;<DT>2 <DD>for he founded it upon the seas and established it upon the waters. <DT>3 <DD>Who may ascend the hill of the LORD? Who may stand in his holy place?<DT>4 <DD>He who has clean hands and a pure heart, who does not lift up his soul to an idol or swear by what is false. <sup>[<a href="#footnote_102600528_1">1</a>]</sup>  <DT>5 <DD>He will receive blessing from the LORD and vindication from God his Savior.<DT>6 <DD>Such is the generation of those who seek him, who seek your face, O God of Jacob. <sup>[<a href="#footnote_102600528_2">2</a>]</sup>    Selah <DT>7 <DD>Lift up your heads, O you gates; be lifted up, you ancient doors, that the King of glory may come in.<DT>8 <DD>Who is this King of glory? The LORD strong and mighty, the LORD mighty in battle.<DT>9 <DD>Lift up your heads, O you gates; lift them up, you ancient doors, that the King of glory may come in.<DT>10 <DD>Who is he, this King of glory? The LORD Almighty-- he is the King of glory. Selah </DL><OL><LI><A NAME="footnote_102600528_1">[4] Or <I>swear falsely</I></A></LI>
<LI><A NAME="footnote_102600528_2">[6] Two Hebrew manuscripts and Syriac (see also Septuagint); most Hebrew manuscripts <I>face, Jacob</I></A></LI>
</OL>
<OL></OL>
<BR>
<BR>
</TR>

</BODY>
</HTML>
"""

m = re.search(r'</DL>.*?</DL>', html_content, re.DOTALL)
s = m.start() + len('</DL>')
e = m.end() - len('</DL>')
verses_html = html_content[s:e].strip()

m = re.search(r'<OL>.*?</OL>', html_content, re.DOTALL)
s = m.start() + len('<OL>')
e = m.end() - len('</OL>')
footnotes_html = html_content[s:e].strip()

# print(verses_html)
# print(footnotes_html)

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

print('Footnotes:', footnotes_html_to_array(footnotes_html))
print('\n')

sys.exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract Psalm title
title = soup.find('b').get_text(strip=True) if soup.find('b') else "Unknown Title"
# print(title)

# # Insert a </DD> before every <DT>
# for dt in soup.find_all('dt'):
#     dt.insert_before('</DD>')

all_dds = soup.find_all('dd')


print(len(all_dds))
print(all_dds[5])

# Extract verses
verses = []
for dt, dd in zip(soup.find_all('dt'), soup.find_all('dd')):
    verse_number = dt.get_text(strip=True)
    verse_text = dd.get_text(strip=True)
    # print(verse_text, '\n---')

# Extract footnotes
footnotes = []
for li in soup.find_all('li'):
    footnote_text = li.get_text(strip=True)
    footnotes.append(footnote_text)
