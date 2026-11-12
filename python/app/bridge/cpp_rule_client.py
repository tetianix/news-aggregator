import json
import urllib.request
from typing import List

from app.models.article import Article


class CppRuleClient:
    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")

    def filter(self, articles: List[Article], keyword: str) -> List[Article]:
        payload = {
            "keyword": keyword.lower(),
            "articles": [
                {"id": article.id, "text": f"{article.title} {article.text}".lower()}
                for article in articles
            ],
        }
        request = urllib.request.Request(
            f"{self._base_url}/filter",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.loads(response.read())
        matched = set(result["matched"])
        return [article for article in articles if article.id in matched]
