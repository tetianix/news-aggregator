from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Dict, List

from app.models.article import Article
from app.sources.base import FeedSource


@dataclass
class LoadResult:
    articles: List[Article] = field(default_factory=list)
    errors: Dict[str, str] = field(default_factory=dict)


class SourceLoader:
    def __init__(self, sources: List[FeedSource], max_workers: int = 8):
        self._sources = sources
        self._max_workers = max_workers

    def load(self) -> LoadResult:
        result = LoadResult()
        if not self._sources:
            return result
        with ThreadPoolExecutor(max_workers=self._max_workers) as pool:
            futures = [(source, pool.submit(source.fetch)) for source in self._sources]
            for source, future in futures:
                try:
                    result.articles.extend(future.result())
                except Exception as error:
                    result.errors[source.name] = str(error) or type(error).__name__
        return result
