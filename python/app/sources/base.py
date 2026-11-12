from abc import ABC, abstractmethod
from typing import List

from app.models.article import Article


class FeedSource(ABC):
    @abstractmethod
    def fetch(self) -> List[Article]:
        pass
