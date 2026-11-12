import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Optional

from app.models.article import Article
from app.sources.base import FeedSource

DC_CREATOR = "{http://purl.org/dc/elements/1.1/}creator"


class RssSource(FeedSource):
    def __init__(self, url: str, name: str):
        self._url = url
        self._name = name

    def fetch(self) -> List[Article]:
        data = self._download()
        return self._parse(data)

    def _download(self) -> bytes:
        request = urllib.request.Request(self._url, headers={"User-Agent": "news-aggregator"})
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.read()

    def _parse(self, data: bytes) -> List[Article]:
        root = ET.fromstring(data)
        articles = []
        for item in root.iter("item"):
            link = self._text(item, "link")
            articles.append(Article(
                id=self._text(item, "guid") or link,
                title=self._text(item, "title"),
                link=link,
                author=self._text(item, "author") or self._text(item, DC_CREATOR),
                published=self._date(self._text(item, "pubDate")),
                source=self._name,
                text=self._clean_html(self._text(item, "description")),
            ))
        return articles

    @staticmethod
    def _text(item: ET.Element, tag: str) -> str:
        value = item.findtext(tag)
        return value.strip() if value else ""

    @staticmethod
    def _date(value: str) -> Optional[datetime]:
        if not value:
            return None
        try:
            return parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _clean_html(value: str) -> str:
        return re.sub(r"<[^>]+>", " ", value).strip()
