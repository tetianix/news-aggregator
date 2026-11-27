from typing import Dict, Type

from app.sources.atom_source import AtomSource
from app.sources.base import FeedSource
from app.sources.http_source import HttpFeedSource
from app.sources.json_feed_source import JsonFeedSource
from app.sources.rss_source import RssSource


class SourceFactory:
    _types: Dict[str, Type[HttpFeedSource]] = {
        "rss": RssSource,
        "atom": AtomSource,
        "json": JsonFeedSource,
    }

    def create(self, config: dict) -> FeedSource:
        source_type = str(config.get("type", "")).lower()
        source_class = self._types.get(source_type)
        if source_class is None:
            raise ValueError(f"Невідомий тип джерела «{source_type}» у {config.get('name', '?')}")
        return source_class(config["url"], config["name"])
