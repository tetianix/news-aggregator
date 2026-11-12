from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.models.article import Article


@dataclass
class Digest:
    title: str
    articles: List[Article]
    created: datetime

    def to_text(self) -> str:
        lines = [self.title, ""]
        if not self.articles:
            lines.append("Нічого не знайдено.")
        for number, article in enumerate(self.articles, start=1):
            lines.append(f"{number}. {article.title}")
            lines.append(article.link)
        return "\n".join(lines)


class DigestBuilder:
    def __init__(self, max_articles: int = 20):
        self._max_articles = max_articles

    def build(self, articles: List[Article], keyword: str) -> Digest:
        now = datetime.now()
        title = f"Дайджест «{keyword}» за {now:%d.%m.%Y}, новин: {len(articles)}"
        return Digest(title=title, articles=articles[: self._max_articles], created=now)
