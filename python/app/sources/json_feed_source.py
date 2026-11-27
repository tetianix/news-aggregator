import json
from datetime import datetime
from typing import List, Optional

from app.models.article import Article
from app.sources.http_source import HttpFeedSource


class JsonFeedSource(HttpFeedSource):
    def _parse(self, data: bytes) -> List[Article]:
        feed = json.loads(data)
        articles = []
        for item in feed.get("items", []):
            text = item.get("content_text") or self._clean_html(item.get("content_html", "")) or item.get("summary", "")
            articles.append(Article(
                id=str(item.get("id") or item.get("url", "")),
                title=item.get("title") or text[:80],
                link=item.get("url", ""),
                author=self._author(item, feed),
                published=self._date(item.get("date_published") or item.get("date_modified")),
                source=self.name,
                text=text,
            ))
        return articles

    @staticmethod
    def _author(item: dict, feed: dict) -> str:
        authors = item.get("authors") or feed.get("authors") or []
        if authors:
            return authors[0].get("name", "")
        author = item.get("author") or feed.get("author") or {}
        return author.get("name", "")

    @staticmethod
    def _date(value: Optional[str]) -> Optional[datetime]:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
