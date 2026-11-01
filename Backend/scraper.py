import re
import feedparser
from bs4 import BeautifulSoup

RSS_FEEDS = [
    {"url": "https://techcrunch.com/category/artificial-intelligence/feed/", "source": "TechCrunch"},
    {"url": "https://news.ycombinator.com/rss", "source": "Hacker News"},
    {"url": "https://www.producthunt.com/feed", "source": "Product Hunt"},
]

ENTRIES_PER_FEED = 6
MIN_SUMMARY_WORDS = 3


def clean_summary(raw):
    """Return the summary as plain text, or None if it is empty or too short."""
    if not raw:
        return None
    soup = BeautifulSoup(raw, "html.parser")
    for link in soup.find_all("a"):
        link.decompose()
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s\|\s", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" |")
    if len(text.split()) < MIN_SUMMARY_WORDS:
        return None
    return text


def fetch_articles():
    articles = []
    for feed in RSS_FEEDS:
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries[:ENTRIES_PER_FEED]:
            url = entry.get("link")
            if not url:
                continue
            articles.append({
                "title": entry.get("title", "No title found"),
                "summary": clean_summary(entry.get("summary")),
                "url": url,
                "source": feed["source"],
            })
    return articles


if __name__ == "__main__":
    articles = fetch_articles()
    for feed in RSS_FEEDS:
        source = feed["source"]
        items = [a for a in articles if a["source"] == source]
        empty = sum(1 for a in items if a["summary"] is None)
        print(f"{source}: {len(items)} articles, {empty} without summary")
        for a in items[:2]:
            print("  title:  ", a["title"])
            print("  summary:", (a["summary"] or "None")[:150])
        print("-" * 50)