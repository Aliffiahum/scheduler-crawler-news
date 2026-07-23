from app.collector.rss_fetcher import RSSFetcher
from app.collector.rss_parser import RSSParser

fetcher = RSSFetcher()
parser = RSSParser()

xml = fetcher.fetch(
    "https://www.antaranews.com/rss/terkini.xml"
)

news = parser.parse(xml)

print("=" * 50)
print("Jumlah berita :", len(news))
print("=" * 50)

print(news[0])