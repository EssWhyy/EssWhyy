import feedparser
from bs4 import BeautifulSoup
from pathlib import Path

RSS_URL = "https://letterboxd.com/schaffrillas/rss/"  # change to yours
README_PATH = Path("README.md")

START_MARKER = "<!-- LETTERBOXD_START -->"
END_MARKER = "<!-- LETTERBOXD_END -->"


def get_latest_movies(limit=3):
    feed = feedparser.parse(RSS_URL)
    movies = []

    for entry in feed.entries[:limit]:
        title = entry.title
        link = entry.link
        description_html = entry.description

        soup = BeautifulSoup(description_html, "html.parser")
        img = soup.find("img")
        img_src = img["src"] if img else ""

        movies.append({
            "title": title,
            "link": link,
            "img": img_src
        })

    return movies


def update_readme(movies):
    readme = README_PATH.read_text(encoding="utf-8")

    movie_sections = """
<div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
"""

    for movie in movies:
        movie_sections += f"""
    <div style="text-align: center; width: 180px;">
        <a href="{movie['link']}">
            <img src="{movie['img']}" width="150"><br>
            <strong>{movie['title']}</strong>
        </a>
    </div>
"""

    movie_sections += """
</div>
"""

    new_section = f"""
{START_MARKER}
## 🎬 Schaff's Latest Letterboxd Reviews

{movie_sections}

{END_MARKER}
"""

    before = readme.split(START_MARKER)[0]
    after = readme.split(END_MARKER)[1]

    updated_readme = before + new_section + after
    README_PATH.write_text(updated_readme, encoding="utf-8")



if __name__ == "__main__":
    movies = get_latest_movies(limit=3)
    update_readme(movies)
