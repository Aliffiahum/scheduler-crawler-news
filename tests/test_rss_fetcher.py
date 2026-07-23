from app.collector.rss_fetcher import RSSFetcher

fetcher = RSSFetcher()

xml = fetcher.fetch(
    "https://www.antaranews.com/rss/terkini.xml"
)

print(xml[:1000])