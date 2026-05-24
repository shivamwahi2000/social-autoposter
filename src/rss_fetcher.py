import feedparser
import random
from typing import Optional


def fetch_article(feeds: list[str]) -> Optional[dict]:
    """Fetch a random recent article from the provided RSS feeds."""
    shuffled = feeds[:]
    random.shuffle(shuffled)

    for feed_url in shuffled:
        try:
            feed = feedparser.parse(feed_url)
            if not feed.entries:
                continue
            entry = feed.entries[0]
            summary = entry.get("summary", entry.get("description", ""))
            # Strip HTML tags crudely if present
            if "<" in summary:
                import re
                summary = re.sub(r"<[^>]+>", "", summary)
            return {
                "title": entry.get("title", "").strip(),
                "summary": summary.strip()[:600],
                "link": entry.get("link", ""),
                "source": feed.feed.get("title", feed_url),
            }
        except Exception as e:
            print(f"Failed to parse feed {feed_url}: {e}")
            continue

    return None
