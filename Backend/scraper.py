import feedparser
RSS_FEEDS = [
    {
        "url" : "https://techcrunch.com/category/artificial-intelligence/feed/",
        "source" : "TechCrunch"
    },
    {
        "url" : "https://news.ycombinator.com/rss",
        "source" : "Hacker News"
    },
    {
        "url" : "https://www.producthunt.com/feed",
        "source" : "Product Hunt"
    }
]
def fetch_articles():
    articles = []

    for feed in RSS_FEEDS:
        info = feedparser.parse(feed["url"])
        for feed_info in info.entries[:6]:
            url = feed_info.get("link")
            if not url:
                continue
            articles.append({
                "title": feed_info.get("title","No title found"),
                "summary": feed_info.get("summary"),
                "url": url,
                "source": feed["source"],
            })
    return articles

if __name__ == "__main__":
    articles = fetch_articles()
    for feed in RSS_FEEDS:
        source = feed["source"]
        from_source = [a for a in articles if a["source"] == source]
        print(f"{source}: {len(from_source)} articles")
        if from_source:
            first = from_source[0]
            print("  title:  ", first["title"])
            print("  url:    ", first["url"])
            print("  summary:", (first["summary"] or "None")[:200])
        print("-" * 50)
