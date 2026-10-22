import feedparser
RSS_FEEDS = [
    {
        "url" : "https://techcrunch.com/category/artificial-intelligence/feed/",
        "source" : "Tech Crunch"
    },
    {
        "url" : "https://news.ycombinator.com/rss",
        "source" : "Y Combinator"
    },
    {
        "url" : "https://www.producthunt.com/feed",
        "source" : "Product Hunt"
    }
]
def fetch_article():
    article = []

    for feed in RSS_FEEDS:
        info = feedparser.parse(feed["url"])
        for feed_info in info.entries[:6]:
            article.append({
                "title": feed_info.get("title","No title found"),
                "summary": feed_info.get("summary","No summary found"),
                "url": feed_info.get("link", ""),
                "source": feed["source"],
            })
    return article

if __name__ == "__main__":
    articles = fetch_article()

    for art in articles[:5]:
        print(art)
        print("-"*50)
