import feedparser
from urllib.parse import quote


def get_stock_news(symbol):

    try:

        company = symbol.replace(".NS", "")

        url = (
            f"https://news.google.com/rss/search?"
            f"q={quote(company + ' stock')}"
            f"&hl=en-IN&gl=IN&ceid=IN:en"
        )

        feed = feedparser.parse(url)

        latest_news = []

        for entry in feed.entries[:5]:

            latest_news.append({
                "title": entry.title,
                "publisher": getattr(entry, "source", {}).get("title", "Google News")
                if hasattr(entry, "source") else "Google News",
                "link": entry.link
            })

        return latest_news

    except Exception as e:

        print(e)

        return []