from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from app.models.article import Article


@dataclass
class Digest:
    title: str
    articles: List[Article]
    created: datetime
    per_source: Dict[str, int] = field(default_factory=dict)

    def to_text(self) -> str:
        lines = [self.title]
        if not self.articles:
            lines += ["", "Нічого не знайдено."]
        number = 0
        for source, articles in self._grouped().items():
            lines += ["", f"{source} ({len(articles)})"]
            for article in articles:
                number += 1
                lines.append(f"{number}. {article.title}")
                lines.append(article.link)
        if self.per_source:
            stats = ", ".join(f"{source} — {count}" for source, count in self.per_source.items())
            lines += ["", f"Новин за джерелами: {stats}"]
        return "\n".join(lines)

    def _grouped(self) -> Dict[str, List[Article]]:
        groups: Dict[str, List[Article]] = {}
        for article in self.articles:
            groups.setdefault(article.source, []).append(article)
        return groups


class DigestBuilder:
    def __init__(self, max_articles: int = 20):
        self._max_articles = max_articles

    def build(self, articles: List[Article], keyword: str) -> Digest:
        now = datetime.now()
        ordered = sorted(articles, key=self._sort_key, reverse=True)
        topic = f" «{keyword}»" if keyword else ""
        title = f"Дайджест{topic} за {now:%d.%m.%Y}, новин: {len(articles)}"
        if len(articles) > self._max_articles:
            title += f", показано {self._max_articles}"
        per_source = dict(Counter(article.source for article in articles).most_common())
        return Digest(title=title, articles=ordered[: self._max_articles], created=now, per_source=per_source)

    @staticmethod
    def _sort_key(article: Article) -> float:
        return article.published.timestamp() if article.published else 0.0
