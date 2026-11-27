import html
import re
import urllib.request
from abc import abstractmethod
from typing import List

from app.models.article import Article
from app.sources.base import FeedSource


class HttpFeedSource(FeedSource):
    def __init__(self, url: str, name: str, timeout: int = 15):
        self._url = url
        self._name = name
        self._timeout = timeout

    @property
    def name(self) -> str:
        return self._name

    def fetch(self) -> List[Article]:
        return self._parse(self._download())

    def _download(self) -> bytes:
        request = urllib.request.Request(self._url, headers={"User-Agent": "news-aggregator"})
        with urllib.request.urlopen(request, timeout=self._timeout) as response:
            return response.read()

    @abstractmethod
    def _parse(self, data: bytes) -> List[Article]:
        pass

    @staticmethod
    def _clean_html(value: str) -> str:
        text = re.sub(r"<[^>]+>", " ", value or "")
        return re.sub(r"\s+", " ", html.unescape(text)).strip()
