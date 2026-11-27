import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional

from app.models.article import Article
from app.sources.http_source import HttpFeedSource

ATOM = "{http://www.w3.org/2005/Atom}"


class AtomSource(HttpFeedSource):
    def _parse(self, data: bytes) -> List[Article]:
        root = ET.fromstring(data)
        articles = []
        for entry in root.iter(f"{ATOM}entry"):
            link = self._link(entry)
            articles.append(Article(
                id=self._text(entry, "id") or link,
                title=self._text(entry, "title"),
                link=link,
                author=self._text(entry, "author/name"),
                published=self._date(self._text(entry, "published") or self._text(entry, "updated")),
                source=self.name,
                text=self._clean_html(self._text(entry, "content") or self._text(entry, "summary")),
            ))
        return articles

    @staticmethod
    def _text(entry: ET.Element, path: str) -> str:
        full_path = "/".join(f"{ATOM}{part}" for part in path.split("/"))
        value = entry.findtext(full_path)
        return value.strip() if value else ""

    @staticmethod
    def _link(entry: ET.Element) -> str:
        for link in entry.findall(f"{ATOM}link"):
            if link.get("rel", "alternate") == "alternate":
                return link.get("href", "")
        return ""

    @staticmethod
    def _date(value: str) -> Optional[datetime]:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
