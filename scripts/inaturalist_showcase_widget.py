import requests
import xml.etree.ElementTree as ET
import html
import re
from pathlib import Path
from datetime import datetime

FEED_URL = "https://www.inaturalist.org/observations.atom?user_id=esswhyy"
README_PATH = Path("README.md")

START_MARKER = "<!-- INATURALIST_START -->"
END_MARKER = "<!-- INATURALIST_END -->"

# Fetch feed
response = requests.get(FEED_URL)
response.raise_for_status()

# Parse XML
root = ET.fromstring(response.content)

# Atom namespace
ns = {"atom": "http://www.w3.org/2005/Atom"}

entries = root.findall("atom:entry", ns)[:3]

import requests
import xml.etree.ElementTree as ET
import html
import re
from pathlib import Path
from datetime import datetime

FEED_URL = "https://www.inaturalist.org/observations.atom?user_id=esswhyy"
README_PATH = Path("README.md")

START_MARKER = "<!-- INATURALIST_START -->"
END_MARKER = "<!-- INATURALIST_END -->"

# Fetch feed
response = requests.get(FEED_URL)
response.raise_for_status()

# Parse XML
root = ET.fromstring(response.content)

# Atom namespace
ns = {"atom": "http://www.w3.org/2005/Atom"}

entries = root.findall("atom:entry", ns)[:3]
readme = README_PATH.read_text(encoding="utf-8")

image_cells = []
caption_cells = []

for entry in entries:
    title = entry.find("atom:title", ns).text

    published = entry.find("atom:published", ns).text
    dt = datetime.fromisoformat(published)
    published = dt.strftime("%d %b %Y")

    link_elem = entry.find("atom:link[@rel='alternate']", ns)
    link = link_elem.attrib["href"] if link_elem is not None else "#"

    content_elem = entry.find("atom:content", ns)
    img_url = ""

    if content_elem is not None and content_elem.text:
        content_html = html.unescape(content_elem.text)
        match = re.search(r'src="([^"]+)"', content_html)
        if match:
            img_url = match.group(1)

    image_cells.append(
        f'<td align="center"><a href="{link}"><img src="{img_url}" width="150"/></a></td>'
    )

    caption_cells.append(
        f'<td align="center">'
        f'<strong><a href="{link}">{title}</a></strong><br/>'
        f'<sub>{published}</sub>'
        f'</td>'
    )

html_block = (
    f"{START_MARKER}\n"
    f"<table>\n"
    f"  <tr>\n"
    f"    {''.join(image_cells)}\n"
    f"  </tr>\n"
    f"  <tr>\n"
    f"    {''.join(caption_cells)}\n"
    f"  </tr>\n"
    f"</table>\n"
    f"{END_MARKER}"
)

before = readme.split(START_MARKER)[0]
after = readme.split(END_MARKER)[1]

updated_readme = before + html_block + after
README_PATH.write_text(updated_readme, encoding="utf-8")