from abc import ABC, abstractmethod
from typing import List

from app.models.article import Article


class FeedSource(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def fetch(self) -> List[Article]:
        pass
